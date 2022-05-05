import json
import boto3
import requests
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('linkStorage')


def handler(event,context):
    try:
        prefix = event['requestContext']['domainPrefix']
        path = event["pathParameters"]['link']
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
        if event['httpMethod'] == 'GET':
            return {
                "statusCode": 301,
                "headers": {'Location':long_url}
            }
        elif event['httpMethod'] == 'POST' and long_url != "https://basementremodeling.com/404":
            print(event['body'])
            requests.post(long_url, json=event['body'])
            return {"statusCode" : 200}
        return {"statusCode" : 400}