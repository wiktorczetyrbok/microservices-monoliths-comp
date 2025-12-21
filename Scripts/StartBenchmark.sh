#!/bin/bash
set -e

languages=("java" "js" "python")
app_types=("monolith" "microservices-grpc")

for language in "${languages[@]}"; do
  for app_type in "${app_types[@]}"; do
    stack_name="${language}-${app_type}"

    ssh -i ./ssh_key -o StrictHostKeyChecking=no wczetyrbok@10.0.0.2 "
      sudo docker stack deploy -c app/Repositories/$language/$language-$app_type/docker-compose.yml $stack_name --with-registry-auth
    "
    sleep 30
    
    if [ "$app_type" == "monolith" ]; then
      service_names=('gateway')
    else
      service_names=('gateway' 'search' 'profile' 'geo' 'rate')
    fi
    for service in "${service_names[@]}"; do
      ssh -i ./ssh_key -o StrictHostKeyChecking=no wczetyrbok@10.0.0.2 "
        sudo docker service scale ${stack_name}_${service}=5
      "
    done
    
      
    sleep 10


    url="http://10.0.0.2:5000/hotels?inDate=2023-06-07&outDate=2023-06-12&lat=54.29&lon=18.55"
    while true; do
        status=$(curl -s -o /dev/null -w "%{http_code}" "$url")
        if [ "$status" -eq 200 ]; then
            echo "Service ready"
            break
        else
            echo "Service not running"
            sleep 5
        fi
    done

    if [ "$language" == "python" ]; then
      bash run_Jmeter.sh 3 1 1 100 $language $app_type > /dev/null 2>&1
    elif [ "$app_type" == "monolith" ]; then
      bash run_Jmeter.sh 5 5 5 5 $language $app_type > /dev/null 2>&1
      bash run_Jmeter.sh 5 10 10 1250 $language $app_type > /dev/null 2>&1
    elif [ "$app_type" == "microservices-grpc" ]; then
      bash run_Jmeter.sh 5 5 5 5 $language $app_type > /dev/null 2>&1
      bash run_Jmeter.sh 5 10 10 600 $language $app_type > /dev/null 2>&1
    else
      bash run_Jmeter.sh 5 5 5 5 $language $app_type > /dev/null 2>&1
      bash run_Jmeter.sh 5 10 10 350 $language $app_type > /dev/null 2>&1
    fi

    ssh -i ./ssh_key -o StrictHostKeyChecking=no wczetyrbok@10.0.0.2 "
      sudo docker service ls -q | xargs -r docker service rm
    "
    sleep 30
    echo "[$(date)] 🚀 COMPLETED scenario: $language / $app_type"

  done
done
