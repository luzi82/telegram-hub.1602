#!/bin/bash

PROJECT_ROOT_PATH=${PWD}

cd ${PROJECT_ROOT_PATH}
aws dynamodb delete-table \
    --table-name tmp_table \
    --endpoint-url http://localhost:8000 \
    --region `cat local-test-tmp/region` || true
aws dynamodb create-table \
    --table-name tmp_table \
    --attribute-definitions file://local-test-tmp/db.AttributeDefinitions \
    --key-schema file://local-test-tmp/db.KeySchema \
    --global-secondary-indexes file://local-test-tmp/db.GlobalSecondaryIndexes \
    --billing-mode file://local-test-tmp/db.BillingMode \
    --endpoint-url http://localhost:8000 \
    --region `cat local-test-tmp/region`
python3 unit_test/db_test.py
