#!/bin/bash

set -Eeuo pipefail

############# GLOBAL VARIABLES
declare BASH_SRC_rk="$(dirname ${BASH_SOURCE[0]})"

declare RUN_REDIS

declare DOCKER_IMAGE_NAME="redis:latest"
declare CONTAINER_NAME="redis"
declare BROKER_DOCKER_NETWORK="broker-net"

############# FUNCTIONS
function usage() {
    cat <<EOF
        $(basename $0) [OPTIONS]

    OPTIONS:
        -h          Display this help menu and exit
        -d          Debug mode
        -r          Run
EOF

    exit 1
}

function run_redis() {
    docker run -dt --name ${CONTAINER_NAME} -p 6379:6379 \
	--network ${BROKER_DOCKER_NETWORK} \
        ${DOCKER_IMAGE_NAME}

    return $?
}

############# MAIN CODE
[ $# -lt 1 ] && usage

while [[ $# -gt 0 ]]; do
    case "${1:-}" in
        -h) usage ;;
        -d) set -x ;;
        -r) RUN_REDIS='y' ;;
    esac
    shift
done

if [ -n "${RUN_REDIS:-}" ]; then
    if docker container inspect ${CONTAINER_NAME} > /dev/null 2>&1; then
        docker start ${CONTAINER_NAME}
    else
        run_redis
    fi
fi

exit 0

