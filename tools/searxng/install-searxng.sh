#!/usr/bin/env bash
set -euo pipefail

# Local Docker-based SearXNG install for development and teaching use.

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
  printf '[install] %s\n' "$1"
}

fail() {
  printf '[install] ERROR: %s\n' "$1" >&2
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

generate_secret() {
  if command -v openssl >/dev/null 2>&1; then
    openssl rand -hex 32
    return
  fi

  od -An -N 32 -tx1 /dev/urandom | tr -d ' \n'
}

write_settings_file() {
  local secret_key

  mkdir -p "$INSTALL_DIR"
  secret_key=$(generate_secret)

  # Keep the generated config small so the important SearXNG settings stay visible.
  cat > "$CONFIG_FILE" <<SETTINGS
use_default_settings: true

general:
  debug: false

search:
  formats:
    - html
    - json

server:
  bind_address: "0.0.0.0"
  port: 8080
  secret_key: "${secret_key}"
  limiter: false
SETTINGS
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

  printf '\n[install] Recent container logs:\n' >&2
  docker logs --tail 40 "$CONTAINER_NAME" >&2 || true
  rm -f "$response_file"
  fail "SearXNG did not become ready at ${SMOKE_TEST_URL}"
}

main() {
  require_command docker
  require_command curl

  if ! docker info >/dev/null 2>&1; then
    fail "Docker is installed, but the Docker daemon is not reachable."
  fi

  log "Writing local SearXNG settings to ${CONFIG_FILE}"
  write_settings_file

  if container_exists; then
    log "Removing existing container ${CONTAINER_NAME} so the install starts cleanly"
    docker rm -f "$CONTAINER_NAME" >/dev/null
  fi

  # Check for an occupied port before starting the container so the error is easy to understand.
  if port_in_use; then
    fail "Host port ${HOST_PORT} is already in use. Set SEARXNG_PORT to a free port and try again."
  fi

  log "Pulling Docker image ${IMAGE_NAME}"
  docker pull "$IMAGE_NAME"

  # Mount the generated settings file so the container stays easy to inspect locally.
  log "Starting SearXNG on ${BASE_URL}"
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

  log "Install complete."
  log "Local endpoint: ${BASE_URL}"
  log "Example JSON query: ${SMOKE_TEST_URL}"
}

main "$@"
