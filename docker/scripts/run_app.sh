#!/bin/bash

set -Eeuo pipefail

############# GLOBAL VARIABLES
declare BASH_SRC_rapp="$(dirname ${BASH_SOURCE[0]})"
declare ROOT_REPO_PATH="${BASH_SRC_rapp}/../.."
declare DOCKER_PATH="${ROOT_REPO_PATH}/docker"

declare ORCHEST_YML="${DOCKER_PATH}/orchestrator.yml"
declare ENV_FILE="${DOCKER_PATH}/config.env"
declare KAFKA_CLUSTER=$(mktemp -dt KAFKA_XXXX)
declare CLUSTER_ID

############# FUNCTIONS
function get_env_file_variable() {
	local var_name="${1}"

	cat ${ENV_FILE} | grep -v '#' | grep -w ${var_name} | cut -d '=' -f 2 | xargs

	return $?
}

function get_cluster_id() {
    docker run -ti --rm \
        ${KAFKA_IMG_NAME} \
        /bin/bash -c "kafka-storage random-uuid"

    return $?
}

function init_cluster() {
    local cluster_id="${1}"
    
    docker run --rm \
        -v ${KAFKA_CLUSTER}:${KAFKA_DOCKER_LOG} \
        ${KAFKA_IMG_NAME} \
        kafka-storage format --cluster-id "${cluster_id}" \
        --config /etc/kafka/kafka.properties

    return $?
}

############# MAIN CODE
declare KAFKA_IMG_NAME="$(get_env_file_variable "KAFKA__IMG_NAME")"
declare KAFKA_DOCKER_LOG="$(get_env_file_variable "KAFKA__DOCKER_LOG")"

CLUSTER_ID="" KAFKA_CLUSTER="${KAFKA_CLUSTER}" \
	docker compose --env-file "${ENV_FILE}" -f ${ORCHEST_YML} build kafka

CLUSTER_ID="$(get_cluster_id)"
init_cluster ${CLUSTER_ID}
chown -R 1000:1000 ${KAFKA_CLUSTER}

CLUSTER_ID="${CLUSTER_ID}" KAFKA_CLUSTER="${KAFKA_CLUSTER}" \
	docker compose --env-file "${ENV_FILE}" -f ${ORCHEST_YML} up --build

exit 0

