gcloud compute scp \
  --recurse \
  w_czetyrbok@load-runner-instance:/home/wczetyrbok/app/csv \
  ./csv \
  --zone=europe-west1-b

sudo pkill -f "RunSpecificBenchmark.sh"

sudo bash RunSpecificBenchmark.sh java monolith 3 5 5 150 images && \
sudo bash RunSpecificBenchmark.sh java microservices-grpc 3 5 5 120 images && \
sudo bash RunSpecificBenchmark.sh js monolith 3 5 5 130 images && \
sudo bash RunSpecificBenchmark.sh js microservices-grpc 3 5 5 120 images
sudo bash RunSpecificBenchmark.sh python monolith 3 2 2 30 images && \
sudo bash RunSpecificBenchmark.sh python microservices-grpc 3 1 1 20 images



sudo bash RunSpecificBenchmark.sh java monolith 3 5 5 150 images && \
sudo bash RunSpecificBenchmark.sh java microservices-grpc 3 5 5 120 images && \
sudo bash RunSpecificBenchmark.sh js monolith 3 5 5 130 images && \
sudo bash RunSpecificBenchmark.sh js microservices-grpc 3 5 5 120 images
sudo bash RunSpecificBenchmark.sh python monolith 3 2 2 30 images && \
sudo bash RunSpecificBenchmark.sh python microservices-grpc 3 1 1 20 images && \


sudo bash RunSpecificBenchmark.sh java monolith 3 5 5 150 images && \
sudo bash RunSpecificBenchmark.sh java microservices-grpc 3 5 5 120 images && \
sudo bash RunSpecificBenchmark.sh js monolith 3 5 5 130 images && \
sudo bash RunSpecificBenchmark.sh js microservices-grpc 3 5 5 120 images
sudo bash RunSpecificBenchmark.sh python monolith 3 2 2 30 images && \
sudo bash RunSpecificBenchmark.sh python microservices-grpc 3 1 1 20 images && \


sudo bash RunSpecificBenchmark.sh java monolith 3 5 5 150 images && \
sudo bash RunSpecificBenchmark.sh java microservices-grpc 3 5 5 120 images && \
sudo bash RunSpecificBenchmark.sh js monolith 3 5 5 130 images && \
sudo bash RunSpecificBenchmark.sh js microservices-grpc 3 5 5 120 images
sudo bash RunSpecificBenchmark.sh python monolith 3 2 2 30 images && \
sudo bash RunSpecificBenchmark.sh python microservices-grpc 3 1 1 20 images && \