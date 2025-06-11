#!/bin/bash

set -Eeuo pipefail

############# GLOBAL VARIABLES
declare BASH_SRC_rk="$(dirname ${BASH_SOURCE[0]})"

declare BUILD_DOCKER_IMAGE
declare RUN_KAFKA

declare KAFKA_CLUSTER=$(mktemp -dt KAFKA_XXXX)

declare DOCKER_IMAGE_NAME="kafka_custom:latest"
declare CONTAINER_NAME="kafka"
declare CONTEXT="${BASH_SRC_rk}/.."
declare DOCKERFILE_FILE="${BASH_SRC_rk}/../Dockerfile.kafka"
declare DOCKER_KAFKA_NET="kafka-net"

declare KAFKA_DOCKER_LOG="/tmp/kafka-logs"
declare CLUSTER_ID

############# FUNCTIONS
function usage() {
    cat <<EOF
        $(basename $0) [OPTIONS]

    OPTIONS:
        -h          Display this help menu and exit
        -d          Debug mode
        -r          Run
        --build     Build Kafka image
EOF

    exit 1
}

function build_docker_image() {
    docker build -t ${DOCKER_IMAGE_NAME} -f ${DOCKERFILE_FILE} ${CONTEXT}

    return $?
}

function get_cluster_id() {
    docker run -ti --rm \
        ${DOCKER_IMAGE_NAME} \
        /bin/bash -c "kafka-storage random-uuid"

    return $?
}

function init_cluster() {
    local cluster_id="${1}"
    
    docker run --rm \
        -v ${KAFKA_CLUSTER}:${KAFKA_DOCKER_LOG} \
        ${DOCKER_IMAGE_NAME} \
        kafka-storage format --cluster-id "${cluster_id}" \
        --config /etc/kafka/kafka.properties

    return $?
}

function create_network() {
    docker network create ${DOCKER_KAFKA_NET}
}

function run_kafka() {
    local cluster_id="${1}"

    chown -R 1000:1000 ${KAFKA_CLUSTER}

    # TODO do a controller node too.
    docker run -dt --name ${CONTAINER_NAME} --network ${DOCKER_KAFKA_NET} -p 9092:9092 \
        -v ${KAFKA_CLUSTER}:${KAFKA_DOCKER_LOG} \
        -e KAFKA_PROCESS_ROLES=broker,controller \
        -e KAFKA_NODE_ID=1 \
        -e KAFKA_CONTROLLER_QUORUM_VOTERS=1@kafka:9093 \
        -e KAFKA_CONTROLLER_LISTENER_NAMES=CONTROLLER \
        -e KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT \
        -e KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093 \
        -e KAFKA_INTER_BROKER_LISTENER_NAME=PLAINTEXT \
        -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092 \
        -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
        -e KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR=1 \
        -e KAFKA_TRANSACTION_STATE_LOG_MIN_ISR=1 \
        -e KAFKA_LOG_DIRS=${KAFKA_DOCKER_LOG} \
        -e CLUSTER_ID=${cluster_id} \
        ${DOCKER_IMAGE_NAME}

    return $?
}

############# MAIN CODE
[ $# -lt 1 ] && usage

while [[ $# -gt 0 ]]; do
    case "${1:-}" in
        -h) usage ;;
        -d) set -x ;;
        -r) RUN_KAFKA='y' ;;
        --build) BUILD_DOCKER_IMAGE='y' ;;
    esac
    shift
done

[ -n "${BUILD_DOCKER_IMAGE:-}" ] &&
    build_docker_image

if [ -n "${RUN_KAFKA:-}" ]; then
    CLUSTER_ID="$(get_cluster_id)"
    init_cluster ${CLUSTER_ID}

    if ! docker network ls --filter name=${DOCKER_KAFKA_NET} --format '{{.Name}}' | grep -wq ${DOCKER_KAFKA_NET}; then
        create_network
    fi

    export CLUSTER_ID="${CLUSTER_ID}"
    if docker container inspect ${CONTAINER_NAME} > /dev/null 2>&1; then
        docker start ${CONTAINER_NAME}
    else
        run_kafka ${CLUSTER_ID}
    fi
fi

exit 0

