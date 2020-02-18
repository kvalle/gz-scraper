## What is this?

This is an automated way to get notified by email every time Gamezone.no have new interesting items in stock.

## How to use it

The scraper runs in AWS Lambda every morning, checking for new items from the backlog in DynamoDB.

Use the CLI to view the backlog, and to add/remove items.

This is not intended for general use. If you want use it, you'll need to set up your own 😅

## Setup

- Create an AWS lambda in the console, using the Python 3.7 environment. (Haven't scripted this yet…) Make sure to increase the timeout, set the `GZ_SCRAPER_EMAIL_PASSWORD` environment variable, and give the generated role access to DynamoDB.

- Update the ARN for the lambda in `deploy-lambda.sh`

- Create a new trigger event (every day at 9 AM UTC)

  ```bash
  aws events put-rule --region eu-north-1 --name "gz-scraper-trigger" --schedule-expression "cron(0 9 * * ? *)"
  ```

- Add the lambda as target

  ```bash
  aws events put-targets --rule "gz-scraper-trigger" --targets "Id"="1","Arn"="arn:aws:lambda:eu-north-1:017978203355:function:gz-scraper"
  ```

- Optional: check that the trigger looks okay

  ```bash
  aws --region=eu-north-1 events describe-rule --name gz-scraper-trigger
  aws --region=eu-north-1 events list-targets-by-rule --rule gz-scraper-trigger
  ```

- Create DynamoDB table

  ```bash
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
  ```

- Add items to the backlog in DynamoDB

- Deploy the lambda code

  ```bash
  ./deploy-lambda.sh
  ```
