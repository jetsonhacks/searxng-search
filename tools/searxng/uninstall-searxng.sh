#!/usr/bin/env bash
set -euo pipefail

# Local Docker-based SearXNG uninstall for development and teaching use.

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO_ROOT=$(cd "$SCRIPT_DIR/../.." && pwd)
INSTALL_DIR="$REPO_ROOT/.local/searxng"
CONTAINER_NAME="searxng-search-local"
IMAGE_NAME="searxng/searxng:latest"

log() {
  printf '[uninstall] %s\n' "$1"
}

fail() {
  printf '[uninstall] ERROR: %s\n' "$1" >&2
  exit 1
}

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    fail "Required command not found: $1"
  fi
}

container_exists() {
  docker container inspect "$CONTAINER_NAME" >/dev/null 2>&1
}

main() {
  require_command docker

  if ! docker info >/dev/null 2>&1; then
    fail "Docker is installed, but the Docker daemon is not reachable."
  fi

  if container_exists; then
    log "Removing container ${CONTAINER_NAME}"
    docker rm -f "$CONTAINER_NAME" >/dev/null
  else
    log "Container ${CONTAINER_NAME} is not present"
  fi

  if [ -d "$INSTALL_DIR" ]; then
    log "Removing generated files in ${INSTALL_DIR}"
    rm -rf "$INSTALL_DIR"
  else
    log "Generated directory ${INSTALL_DIR} is not present"
  fi

  if docker image inspect "$IMAGE_NAME" >/dev/null 2>&1; then
    log "Trying to remove image ${IMAGE_NAME} as a best-effort cleanup step"
    if docker image rm "$IMAGE_NAME" >/dev/null 2>&1; then
      log "Removed image ${IMAGE_NAME}"
    else
      log "Left image ${IMAGE_NAME} in place because Docker reported it is still in use or shared"
    fi
  else
    log "Image ${IMAGE_NAME} is not present"
  fi

  log "Uninstall complete."
}

main "$@"
