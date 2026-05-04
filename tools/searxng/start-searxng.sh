#!/usr/bin/env bash
set -euo pipefail

# Restart the local Docker-based SearXNG instance after it has been stopped
# or after the container has been pruned.

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO_ROOT=$(cd "$SCRIPT_DIR/../.." && pwd)
INSTALL_DIR="$REPO_ROOT/.local/searxng"
CONFIG_FILE="$INSTALL_DIR/settings.yml"
CONTAINER_NAME="searxng-search-local"
IMAGE_NAME="searxng/searxng:latest"
HOST_PORT="${SEARXNG_PORT:-8080}"
BASE_URL="http://127.0.0.1:${HOST_PORT}"
SMOKE_TEST_URL="${BASE_URL}/search?q=smoke+test&format=json"
SMOKE_TEST_ATTEMPTS=30
SMOKE_TEST_DELAY_SECONDS=2

log() {
  printf '[start] %s\n' "$1"
}

fail() {
  printf '[start] ERROR: %s\n' "$1" >&2
  exit 1
}

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    fail "Required command not found: $1"
  fi
}

port_in_use() {
  if ! command -v ss >/dev/null 2>&1; then
    return 1
  fi

  ss -ltnH "( sport = :${HOST_PORT} )" | grep -q .
}

container_exists() {
  docker container inspect "$CONTAINER_NAME" >/dev/null 2>&1
}

container_running() {
  [ "$(docker container inspect --format '{{.State.Running}}' "$CONTAINER_NAME")" = "true" ]
}

wait_for_smoke_test() {
  local attempt
  local response_file

  response_file=$(mktemp)

  # Wait until the local JSON endpoint responds before reporting success.
  for ((attempt = 1; attempt <= SMOKE_TEST_ATTEMPTS; attempt += 1)); do
    log "Smoke test attempt ${attempt}/${SMOKE_TEST_ATTEMPTS}: ${SMOKE_TEST_URL}"

    if curl --silent --show-error --fail --max-time 10 "$SMOKE_TEST_URL" >"$response_file"; then
      if grep -q '"results"' "$response_file"; then
        rm -f "$response_file"
        log "SearXNG responded with JSON search results."
        return 0
      fi

      rm -f "$response_file"
      fail "Endpoint responded, but the smoke test did not detect JSON output."
    fi

    sleep "$SMOKE_TEST_DELAY_SECONDS"
  done

  printf '\n[start] Recent container logs:\n' >&2
  docker logs --tail 40 "$CONTAINER_NAME" >&2 || true
  rm -f "$response_file"
  fail "SearXNG did not become ready at ${SMOKE_TEST_URL}"
}

start_existing_container() {
  if container_running; then
    log "Container ${CONTAINER_NAME} is already running."
    wait_for_smoke_test
    return
  fi

  if port_in_use; then
    fail "Host port ${HOST_PORT} is already in use. Set SEARXNG_PORT to a free port and try again."
  fi

  log "Starting existing container ${CONTAINER_NAME}"
  docker start "$CONTAINER_NAME" >/dev/null
  wait_for_smoke_test
}

create_container() {
  if [ ! -f "$CONFIG_FILE" ]; then
    fail "Missing ${CONFIG_FILE}. Run tools/searxng/install-searxng.sh before starting SearXNG."
  fi

  if ! docker image inspect "$IMAGE_NAME" >/dev/null 2>&1; then
    fail "Missing Docker image ${IMAGE_NAME}. Run tools/searxng/install-searxng.sh to pull the image."
  fi

  if port_in_use; then
    fail "Host port ${HOST_PORT} is already in use. Set SEARXNG_PORT to a free port and try again."
  fi

  log "Creating container ${CONTAINER_NAME} from existing local config"
  if ! docker run \
    --detach \
    --name "$CONTAINER_NAME" \
    --publish "${HOST_PORT}:8080" \
    --volume "$CONFIG_FILE:/etc/searxng/settings.yml:ro" \
    --restart unless-stopped \
    "$IMAGE_NAME" >/dev/null; then
    if port_in_use; then
      fail "Docker could not bind host port ${HOST_PORT}. Set SEARXNG_PORT to a free port and try again."
    fi

    fail "Docker could not start the ${CONTAINER_NAME} container."
  fi

  wait_for_smoke_test
}

main() {
  require_command docker
  require_command curl

  if ! docker info >/dev/null 2>&1; then
    fail "Docker is installed, but the Docker daemon is not reachable."
  fi

  if container_exists; then
    start_existing_container
  else
    create_container
  fi

  log "SearXNG is running."
  log "Local endpoint: ${BASE_URL}"
  log "Example JSON query: ${SMOKE_TEST_URL}"
}

main "$@"
