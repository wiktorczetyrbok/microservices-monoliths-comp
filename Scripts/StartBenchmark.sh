#!/bin/bash
set -e
machine="$1"

languages=("java" "js" "python")
app_types=("monolith" "microservices-grpc")

for language in "${languages[@]}"; do
  for app_type in "${app_types[@]}"; do
    stack_name="${language}-${app_type}-images"

    ssh -i ./ssh_key -o StrictHostKeyChecking=no wczetyrbok@10.0.0.2 "
      sudo docker stack deploy -c app/Repositories/$language/$language-$app_type-images/docker-compose.yml $stack_name
    "
    sleep 30



    url="http://10.0.0.2:5000/images/search?threshold=1.0&kernel=3"
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

    if [ "$machine" == "c2d-2" ]; then

      if [ "$language" == "python" ] && [ "$app_type" == "monolith" ]; then
        bash run_Jmeter_images.sh 3 2 2 30 python monolith

      elif [ "$language" == "python" ] && [ "$app_type" == "microservices-grpc" ]; then
        bash run_Jmeter_images.sh 3 1 1 20 python microservices-grpc

      elif [ "$language" == "java" ] && [ "$app_type" == "monolith" ]; then
        #bash run_Jmeter_images.sh 3 10 5 150 java monolith
        :

      elif [ "$language" == "java" ] && [ "$app_type" == "microservices-grpc" ]; then
        #bash run_Jmeter_images.sh 3 10 5 120 java microservices-grpc
        :

      elif [ "$language" == "js" ] && [ "$app_type" == "monolith" ]; then
        bash run_Jmeter_images.sh 3 5 5 130 js monolith

      elif [ "$language" == "js" ] && [ "$app_type" == "microservices-grpc" ]; then
        bash run_Jmeter_images.sh 3 5 5 120 js microservices-grpc

      else
        exit 1
      fi

    elif [ "$machine" == "c2d-4" ]; then

      if [ "$language" == "python" ] && [ "$app_type" == "monolith" ]; then
        bash run_Jmeter_images.sh 3 2 4 50 python monolith

      elif [ "$language" == "python" ] && [ "$app_type" == "microservices-grpc" ]; then
        bash run_Jmeter_images.sh 3 2 2 30 python microservices-grpc

      elif [ "$language" == "java" ] && [ "$app_type" == "monolith" ]; then
        bash run_Jmeter_images.sh 3 10 10 300 java monolith

      elif [ "$language" == "java" ] && [ "$app_type" == "microservices-grpc" ]; then
        bash run_Jmeter_images.sh 3 20 10 250 java microservices-grpc

      elif [ "$language" == "js" ] && [ "$app_type" == "monolith" ]; then
        bash run_Jmeter_images.sh 3 10 10 250 js monolith

      elif [ "$language" == "js" ] && [ "$app_type" == "microservices-grpc" ]; then
        bash run_Jmeter_images.sh 3 10 10 200 js microservices-grpc

      else
        exit 1
      fi

    elif [ "$machine" == "c2d-8" ]; then

      if [ "$language" == "python" ] && [ "$app_type" == "monolith" ]; then
        bash run_Jmeter_images.sh 3 2 8 100 python monolith

      elif [ "$language" == "python" ] && [ "$app_type" == "microservices-grpc" ]; then
        bash run_Jmeter_images.sh 3 2 4 60 python microservices-grpc

      elif [ "$language" == "java" ] && [ "$app_type" == "monolith" ]; then
        bash run_Jmeter_images.sh 3 20 20 600 java monolith

      elif [ "$language" == "java" ] && [ "$app_type" == "microservices-grpc" ]; then
        bash run_Jmeter_images.sh 3 20 20 500 java microservices-grpc

      elif [ "$language" == "js" ] && [ "$app_type" == "monolith" ]; then
        bash run_Jmeter_images.sh 3 20 20 500 js monolith

      elif [ "$language" == "js" ] && [ "$app_type" == "microservices-grpc" ]; then
        bash run_Jmeter_images.sh 3 10 15 450 js microservices-grpc

      else
        exit 1
      fi

    else
      exit 1
    fi


    ssh -i ./ssh_key -o StrictHostKeyChecking=no wczetyrbok@10.0.0.2 "
      sudo docker service ls -q | xargs -r docker service rm
    "
    sleep 30
    echo "[$(date)] 🚀 COMPLETED scenario: $language / $app_type"

  done
done
