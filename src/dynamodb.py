from pprint import pprint
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
table = dynamodb.Table('gz-scrape-backlog')

def get_backlog():
    response = table.query(
        KeyConditionExpression=Key('for_sale').eq('false')
    )
    return response["Items"]


def mark_as_found(item):
    item['for_sale'] = 'true'
    table.put_item(Item=item)
    table.delete_item(
        Key={
            'game_name': item['game_name'],
            'for_sale': 'false'
        }
    )
