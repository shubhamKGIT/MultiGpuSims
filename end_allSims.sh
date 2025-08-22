#!/usr/bin/env bash
set -euo pipefail

# Resolve project root
PROJECT_ROOT="${SIMS_ROOT:-$(pwd)}"

MULTI_COMPOSE="${PROJECT_ROOT}/multiSim/docker-compose.yml"
SINGLE_COMPOSE="${PROJECT_ROOT}/singleSim/docker-compose.yml"

# Choose docker compose command
if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  COMPOSE="docker compose"
elif command -v docker-compose >/dev/null 2>&1; then
  COMPOSE="docker-compose"
else
  echo "ERROR: docker compose not found."
  exit 1
fi

echo "Stopping CARLA simulations under project root: ${PROJECT_ROOT}"
echo "Using compose tool: ${COMPOSE}"
echo "-------------------------------------"

# Stop multiSim stack if compose file exists
if [[ -f "$MULTI_COMPOSE" ]]; then
  echo "Bringing down multiSim stack..."
  $COMPOSE -f "$MULTI_COMPOSE" down || true
else
  echo "No multiSim docker-compose.yml found."
fi

# Stop singleSim stack if compose file exists
if [[ -f "$SINGLE_COMPOSE" ]]; then
  echo "Bringing down singleSim stack..."
  $COMPOSE -f "$SINGLE_COMPOSE" down || true
else
  echo "No singleSim docker-compose.yml found."
fi

# Catch-all: stop any running containers with "carla" in their name
CARLA_CONTAINERS=$(docker ps -q --filter "name=carla")
if [[ -n "$CARLA_CONTAINERS" ]]; then
  echo "Stopping leftover CARLA containers..."
  docker stop $CARLA_CONTAINERS || true
fi

echo "✅ All CARLA simulation containers terminated."
