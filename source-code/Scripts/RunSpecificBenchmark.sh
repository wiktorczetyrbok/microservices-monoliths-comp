#!/bin/bash

language="$1"
app_type="$2"
iterations="$3"
start_users="$4"
step_users="$5"
end_users="$6"

if [ "$language" == "jcg" ]; then
  languages=("java" "csharp" "go")
else
  languages=("$language")
fi

if [ "$app_type" == "ALL" ]; then
  app_types=("monolith" "microservices-grpc" "microservices-rest")
else
  app_types=("$app_type")
fi


for lang in "${languages[@]}"; do
  for app in "${app_types[@]}"; do
    echo "Starting benchmark for $lang in $app configuration"

    ssh -i ./ssh_key -o StrictHostKeyChecking=no pkraciuk@10.0.0.2 "
      sudo docker stack deploy -c app/Repositories/$lang/$lang-$app/docker-compose.yml $lang-$app
    "

    url="http://10.0.0.2:5000/hotels?inDate=2023-06-17&outDate=2023-06-21&lat=53.9639&lon=18.5269"
    while true; do
        status=$(curl -s -o /dev/null -w "%{http_code}" "$url")
        if [ "$status" -eq 200 ]; then
            echo "$lang $app Service ready"
            break
        else
            echo "$lang $app Service not running"
            sleep 5
        fi
    done

    bash run_Jmeter.sh $iterations $start_users $step_users $end_users > /dev/null 2>&1

    mkdir app
    sudo mkdir -p app/$lang-$app
    sudo mv csv app/$lang-$app/

    ssh -i ./ssh_key -o StrictHostKeyChecking=no pkraciuk@10.0.0.2 "
      sudo docker service ls -q | xargs -r docker service rm
    "
    sleep 10

  done
done
