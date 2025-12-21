#!/usr/bin/env bash
set -e

GH_USER="wiktorczetyrbok"
TOKEN_FILE="$HOME/.ghcr_token"

BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "🔐 Logging in to GHCR..."
cat "$TOKEN_FILE" | docker login ghcr.io -u "$GH_USER" --password-stdin

build_and_push_compose () {
  NAME="$1"
  COMPOSE_FILE="$2"

  echo
  echo "=============================================="
  echo "Building & pushing via Docker Compose: $NAME"
  echo "Compose file: $COMPOSE_FILE"
  echo "=============================================="

  docker compose -f "$COMPOSE_FILE" build
  docker compose -f "$COMPOSE_FILE" push
}

# ==================================================
# PYTHON — MICROSERVICES (gRPC)
# ==================================================
build_and_push_compose "python-microservices-grpc" \
  "$BASE_DIR/Repositories/python/python-microservices-grpc/docker-compose.yml"

# ==================================================
# PYTHON — MONOLITH
# ==================================================
build_and_push_compose "python-monolith" \
  "$BASE_DIR/Repositories/python/python-monolith/docker-compose.yml"

# ==================================================
# JAVA — MICROSERVICES (gRPC)
# ==================================================
build_and_push_compose "java-microservices-grpc" \
  "$BASE_DIR/Repositories/java/java-microservices-grpc/docker-compose.yml"

# ==================================================
# JAVA — MONOLITH
# ==================================================
build_and_push_compose "java-monolith" \
  "$BASE_DIR/Repositories/java/java-monolith/docker-compose.yml"

# ==================================================
# JS — MICROSERVICES (gRPC)
# ==================================================
build_and_push_compose "js-microservices-grpc" \
  "$BASE_DIR/Repositories/js/js-microservices-grpc/docker-compose.yml"

# ==================================================
# JS — MONOLITH
# ==================================================
build_and_push_compose "js-monolith" \
  "$BASE_DIR/Repositories/js/js-monolith/docker-compose.yml"

echo
echo "✅ALL IMAGES BUILT AND PUSHED USING DOCKER COMPOSE"
