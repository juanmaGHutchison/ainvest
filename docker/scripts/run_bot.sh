#!/bin/bash

set -Eeuo pipefail
####### GLOBAL VARIABLES
declare THIS_PATH="$(dirname ${BASH_SOURCE[0]})"
declare DOCKER_IMAGE_NAME="alpaca:1.0"

####### FUNCTIONS
function usage() {
    cat <<EOF
$(basename $0) -r <python_script> [--build]

-r          Bot to trade in Alpaca. MANDATORY
--build     Build Docker image where the bot will run in. OPTIONAL

EXAMPLE:
    $(dirname $0) --build               Builds the docker image
    $(dirname $0) -r main.py            Runs the python bot
    $(dirname $0) -r main.py --build    Builds the docker image and then runs the python bot
EOF

    exit 1
}

####### MAIN CODE
[ $# -lt 1 ] && usage

declare ALPACA_SCRIPT
declare BUILD_DOCKER_IMAGE

while [[ $# -gt 0 ]]; do
    case "${1:-}" in
        -r) ALPACA_SCRIPT="$2"; shift ;;
        --build) BUILD_DOCKER_IMAGE='y' ;;
        *) echo "Unknown option: $1" ; usage ;; 
    esac
    shift
done

[ -n "${BUILD_DOCKER_IMAGE:-}" ] && \
    docker build -t "${DOCKER_IMAGE_NAME}" ${THIS_PATH}/..

if [ -n "${ALPACA_SCRIPT:-}" ]; then
    if [ ! -f ${ALPACA_SCRIPT} ]; then
        echo "Invalid given python script. It is not a file"
        usage
    fi

    docker run -ti --rm \
        -v $(realpath $(dirname ${ALPACA_SCRIPT})):/app \
        --network kafka-net \
        ${DOCKER_IMAGE_NAME} \
        python3 $(basename ${ALPACA_SCRIPT})
fi

exit 0

