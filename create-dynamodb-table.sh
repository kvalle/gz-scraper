#!/usr/bin/env bash

AWS_DEFAULT_REGION=eu-north-1

aws --region eu-north-1 dynamodb create-table \
    --table-name gz-scrape-backlog \
    --attribute-definitions '[
      {
          "AttributeName": "for_sale",
          "AttributeType": "S"
      },
      {
          "AttributeName": "game_name",
          "AttributeType": "S"
      }
    ]' \
    --key-schema '[
      {
          "AttributeName": "for_sale",
          "KeyType": "HASH"
      },
      {
          "AttributeName": "game_name",
          "KeyType": "RANGE"
      }
    ]' \
    --provisioned-throughput '{
      "ReadCapacityUnits": 1,
      "WriteCapacityUnits": 1
    }'
