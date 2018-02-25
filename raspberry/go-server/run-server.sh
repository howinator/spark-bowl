#!/usr/bin/env bash

set -ex

function usage() {
    echo "usage: $0 ENV"
    exit 1
}

if [ $# -ne 1 ]; then
    usage
fi

ENV=$1
export SPARKABOWL_DEPLOY_ENV=$ENV
export SPARKABOWL_PORT="8082"
go run server.go logging.go
