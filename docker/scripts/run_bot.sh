#!/bin/bash

set -Eeuo pipefail
####### GLOBAL VARIABLES
declare THIS_PATH="$(dirname ${BASH_SOURCE[0]})"
declare ROOT_PROJECT_PATH="${THIS_PATH}/../.."
declare SRC_PATH="${ROOT_PROJECT_PATH}/src"
declare DOCKER_PATH="${THIS_PATH}/.."
declare BROKER_DOCKER_NETWORK="broker-net"
declare DOCKER_VERSION_APP="beta"

declare PRODUCER_SCRIPT="${SRC_PATH}/producer.py"
declare PRODUCER_CONTAINER_NAME="producer-$(echo $RANDOM)"
declare PRODUCER_IMAGE_NAME="producer:${DOCKER_VERSION_APP}"
declare PRODUCER_BASE_IMAGE="ubuntu:22.04"
declare DOCKERFILE_PRODUCER="${DOCKER_PATH}/Dockerfile.producer"

declare CONSUMER_SCRIPT="${SRC_PATH}/consumer.py"
declare CONSUMER_IMAGE_NAME="consumer:${DOCKER_VERSION_APP}"
declare CONSUMER_CONTAINER_NAME="consumer-$(echo $RANDOM)"
declare CONSUMER_BASE_IMAGE="tensorflow/tensorflow:2.15.0-gpu"
declare DOCKERFILE_CONSUMER="${DOCKER_PATH}/Dockerfile.consumer"

declare IMAGE_BASE_OUTPUT_NAME="bot_base_image:${DOCKER_VERSION_APP}"
declare DOCKERFILE_BASE="${DOCKER_PATH}/Dockerfile.common"

declare PERSISTENCE_PATH="$(realpath ${ROOT_PROJECT_PATH}/persistence)"

####### FUNCTIONS
function usage() {
    cat <<EOF
$(basename $0) (--producer|--consumer) [--build]

--build     	Build Docker image where the bot will run in. OPTIONAL
-p,--producer	Will launch a producer agent
-c,--consumer	Will launch a consumer agent

EXAMPLE:
    $(dirname $0) -c --build    Builds a consumer
    $(dirname $0) --consumer	Launches a consumer
    $(dirname $0) -c		Launches a consumer
    $(dirname $0) -p --build    Builds the docker image
EOF

    exit 1
}

####### MAIN CODE
[ $# -lt 1 ] && usage

declare RUNNING_SCRIPT
declare BUILD_DOCKER_IMAGE
declare DOCKER_IMAGE_NAME
declare DOCKER_CONTAINER_NAME
declare IMAGE_BASE_NAME
declare IMAGE_INSTANCE_NAME
declare DOCKERFILE_TB_USED
declare DOCKER_ADDITIONAL_PARAMS

while [[ $# -gt 0 ]]; do
    case "${1:-}" in
        --build) BUILD_DOCKER_IMAGE='y' ;;
	-p|--producer)
		RUNNING_SCRIPT="${PRODUCER_SCRIPT}"
		DOCKER_IMAGE_NAME="${PRODUCER_IMAGE_NAME}" ;
		DOCKER_CONTAINER_NAME="${PRODUCER_CONTAINER_NAME}" ;
		IMAGE_BASE_NAME="${PRODUCER_BASE_IMAGE}" ;
		IMAGE_INSTANCE_NAME="${PRODUCER_IMAGE_NAME}" ;
		DOCKERFILE_TB_USED="${DOCKERFILE_PRODUCER}" ;;
	-c|--consumer)
		RUNNING_SCRIPT="${CONSUMER_SCRIPT}"
		DOCKER_IMAGE_NAME="${CONSUMER_IMAGE_NAME}" ;
		DOCKER_CONTAINER_NAME="${CONSUMER_CONTAINER_NAME}" ;
		IMAGE_BASE_NAME="${CONSUMER_BASE_IMAGE}";
		IMAGE_INSTANCE_NAME="${CONSUMER_IMAGE_NAME}" ;
		DOCKERFILE_TB_USED="${DOCKERFILE_CONSUMER}" ;
		DOCKER_ADDITIONAL_PARAMS="--gpus all --runtime=nvidia" ;;
        *) echo "Unknown option: $1" ; usage ;; 
    esac
    shift
done

if [ -n "${BUILD_DOCKER_IMAGE:-}" ]; then
    if [ -z ${IMAGE_BASE_NAME:-} ]; then
	echo "ERROR: Empty base image to build. Set producer/consumer by using (-p|-c) flags"
	usage
    fi
    set -x

    docker build -t "${IMAGE_BASE_OUTPUT_NAME}" \
    	--build-arg BASE_IMAGE=${IMAGE_BASE_NAME} -f ${DOCKERFILE_BASE} ${DOCKER_PATH}

    docker build -t "${IMAGE_INSTANCE_NAME}" \
	--build-arg BASE_IMAGE=${IMAGE_BASE_OUTPUT_NAME} -f ${DOCKERFILE_TB_USED} ${DOCKER_PATH}
else
    declare PERSISTENT_DOCKER_DIR="/$(basename ${PERSISTENCE_PATH})"
    docker run -ti --rm \
        -v $(realpath $(dirname ${RUNNING_SCRIPT})):/app \
	-v ${PERSISTENCE_PATH}:${PERSISTENT_DOCKER_DIR} \
	-e AINVEST_PERSISTENT_DIR=${PERSISTENT_DOCKER_DIR} \
	--name ${DOCKER_CONTAINER_NAME} \
        --network ${BROKER_DOCKER_NETWORK} \
	${DOCKER_ADDITIONAL_PARAMS:-} \
        ${DOCKER_IMAGE_NAME} \
        python3 $(basename ${RUNNING_SCRIPT})
fi

exit 0

