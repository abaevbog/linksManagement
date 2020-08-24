import json
import boto3
import os
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('linkStorage')


def handler(event,context):
    try:
        prefix = event['requestContext']['domainPrefix']
        path = event['path']
        key = f"{prefix}.{path.replace('/','')}"
        response = table.get_item(
        Key={
            'link': key,
            }
        )
        long_url = response['Item']['long_link']
    except KeyError as e:
        print(e)
        long_url = "https://basementremodeling.com/404"
    finally:
        response = {
            "statusCode": 301,
            "headers": {'Location':long_url}
        }
        return response