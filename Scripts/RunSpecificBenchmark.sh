#!/bin/bash

echo "[DEBUG] Script started at $(date)"

BASE_DIR="/home/wczetyrbok/app"
PROGRESS_FILE="$BASE_DIR/progress.json"
STATUS_FILE="$BASE_DIR/status.txt"

echo "RUNNING" > "$STATUS_FILE"

language="$1"
app_type="$2"
iterations="$3"
start_users="$4"
step_users="$5"
end_users="$6"

echo "[DEBUG] Args:"
echo "  language=$language"
echo "  app_type=$app_type"
echo "  iterations=$iterations"
echo "  start_users=$start_users"
echo "  step_users=$step_users"
echo "  end_users=$end_users"

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

TOTAL_SCENARIOS=$((${#languages[@]} * ${#app_types[@]}))
CURRENT_SCENARIO=0

echo "[DEBUG] Languages: ${languages[*]}"
echo "[DEBUG] App types: ${app_types[*]}"
echo "[DEBUG] Total scenarios: $TOTAL_SCENARIOS"

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

    echo "[INFO] 🚀 Starting scenario $CURRENT_SCENARIO/$TOTAL_SCENARIOS: $lang / $app"

    # -------- DEPLOY --------
    STACK_NAME="$lang-$app-images"
    COMPOSE_PATH="app/Repositories/$lang/$lang-$app-images/docker-compose.yml"


    echo "[DEBUG] Deploying stack: $STACK_NAME"
    ssh -i ./ssh_key -o StrictHostKeyChecking=no wczetyrbok@10.0.0.2 "
      sudo docker stack deploy -c $COMPOSE_PATH $STACK_NAME
    "


    url="http://10.0.0.2:5000/images/search?threshold=1.0&kernel=3"


    echo "[DEBUG] Healthcheck URL: $url"

    until [ "$(curl -s -o /dev/null -w "%{http_code}" "$url")" -eq 200 ]; do
      echo "[DEBUG] Service not ready, waiting..."
      sleep 5
    done

    echo "[INFO] Service ready"
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

    echo "[DEBUG] Starting JMeter"

    bash run_Jmeter_images.sh \
      "$iterations" "$start_users" "$step_users" "$end_users" "$lang" "$app"


    echo "[INFO] JMeter finished"

    # -------- CLEANUP --------
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
    echo "[INFO] COMPLETED: $lang / $app "
  done
done

echo "DONE" > "$STATUS_FILE"
echo "[DEBUG] Script finished at $(date)"
