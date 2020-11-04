#!/bin/bash

export PROJECT_PATH="$( cd "$( dirname "$( dirname "${BASH_SOURCE[0]}" )" )" >/dev/null 2>&1 && pwd )"
export SERVERLESS=${PROJECT_PATH}/node_modules/.bin/serverless
export FLASK_APP=src/endpoint.py
