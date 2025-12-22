#!/bin/bash

echo "[DEBUG] Script started at $(date)"

BASE_DIR="/home/wczetyrbok/app"
LOG_FILE="$BASE_DIR/benchmark.log"
PROGRESS_FILE="$BASE_DIR/progress.json"
STATUS_FILE="$BASE_DIR/status.txt"

echo "RUNNING" > "$STATUS_FILE"

language="$1"
app_type="$2"
iterations="$3"
start_users="$4"
step_users="$5"
end_users="$6"

echo "[DEBUG] Args: language=$language app_type=$app_type iterations=$iterations start_users=$start_users step_users=$step_users end_users=$end_users"

if [ "$language" == "all_lang" ]; then
  languages=("java" "python" "js")
else
  languages=("$language")
fi

if [ "$app_type" == "ALL" ]; then
  app_types=("monolith" "microservices-grpc")
else
  app_types=("$app_type")
fi

echo "[DEBUG] Languages resolved: ${languages[@]}"
echo "[DEBUG] App types resolved: ${app_types[@]}"

TOTAL_SCENARIOS=$((${#languages[@]} * ${#app_types[@]}))
CURRENT_SCENARIO=0

for lang in "${languages[@]}"; do
  for app in "${app_types[@]}"; do

    CURRENT_SCENARIO=$((CURRENT_SCENARIO + 1))
    cat <<EOF > "$PROGRESS_FILE"
{
  "current": $CURRENT_SCENARIO,
  "total": $TOTAL_SCENARIOS,
  "language": "$lang",
  "app_type": "$app",
  "phase": "deploying",
  "timestamp": "$(date -Is)"
}
EOF

    echo "[DEBUG] Loop start: lang=$lang app=$app"
    echo "Starting benchmark for $lang in $app configuration"

    echo "[DEBUG] Deploying docker stack $lang-$app"
    ssh -i ./ssh_key -o StrictHostKeyChecking=no wczetyrbok@10.0.0.2 "
      sudo docker stack deploy -c app/Repositories/$lang/$lang-$app/docker-compose.yml $lang-$app
    "

    url="http://10.0.0.2:5000/hotels?inDate=2023-06-07&outDate=2023-06-12&lat=54.29&lon=18.55"
    echo "[DEBUG] Healthcheck URL: $url"
    while true; do
        status=$(curl -s -o /dev/null -w "%{http_code}" "$url")
        echo "[DEBUG] HTTP status=$status"
        if [ "$status" -eq 200 ]; then
            echo "$lang $app Service ready"
            break
        else
            echo "$lang $app Service not running"
            sleep 5
        fi
    done

    cat <<EOF > "$PROGRESS_FILE"
{
  "current": $CURRENT_SCENARIO,
  "total": $TOTAL_SCENARIOS,
  "language": "$lang",
  "app_type": "$app",
  "phase": "jmeter_running",
  "timestamp": "$(date -Is)"
}
EOF

    echo "[DEBUG] Starting JMeter: iterations=$iterations users=$start_users->$end_users step=$step_users"
    bash run_Jmeter.sh $iterations $start_users $step_users $end_users $lang $app
    echo "[DEBUG] JMeter finished for $lang $app"

    cat <<EOF > "$PROGRESS_FILE"
{
  "current": $CURRENT_SCENARIO,
  "total": $TOTAL_SCENARIOS,
  "language": "$lang",
  "app_type": "$app",
  "phase": "cleanup",
  "timestamp": "$(date -Is)"
}
EOF

    echo "[DEBUG] Removing docker services"
    ssh -i ./ssh_key -o StrictHostKeyChecking=no wczetyrbok@10.0.0.2 "
      sudo docker service ls -q | xargs -r docker service rm
    "
    sleep 10
    echo "[$(date)] 🚀 COMPLETED scenario: $language / $app_type"
  done
done

echo "DONE" > "$STATUS_FILE"
echo "[DEBUG] Script finished at $(date)"
