#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
image="${DOCKER_IMAGE:-vasam-generator:local}"
if ! docker image inspect "$image" >/dev/null 2>&1; then
    docker build -t "$image" .
fi
mkdir -p output
if [[ $# -eq 0 ]]; then set -- --area CZ --code-page unicode --en --logging; fi
exec docker run --rm --init --name "${CONTAINER_NAME:-vasam-cz}" \
    --memory="${DOCKER_MEMORY:-7g}" --cpus="${DOCKER_CPUS:-4}" \
    --user "$(id -u):$(id -g)" \
    -e JAVA_MEM="${JAVA_MEM:--Xmx5g}" -e MAX_JOBS="${MAX_JOBS:-2}" \
    -e SEA_URL="${SEA_URL:-https://www.thkukuk.de/osm/data/sea-latest.zip}" \
    -e BOUNDS_URL="${BOUNDS_URL:-https://www.thkukuk.de/osm/data/bounds-latest.zip}" \
    -v "$PWD:/workspace" "$image" "$@"
