import json
import boto3
import os
from random import randint
ROOT_URLS = {'int':os.environ['INTERNAL_URL_ROOT'],'form': os.environ['CLIENT_URL_ROOT']  }
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('linkStorage')

def handler(event,context):
    params = json.loads(event['body'])['parameters']
    output = {}
    for param in params:
        long_link = param['link']
        lead_id = param['lead_id']
        personal_touch = param['personal_touch']
        category = param['category'] #form or int, used as prefix for domain
        tag = param['tag']
        uid = randint(0,10000)
        short_link = f"{category}.{personal_touch}-{uid}"
        table.put_item(
        Item={
                'link': short_link,
                'long_link': long_link,
                'lead_id': lead_id,
                'tag': tag
            }
        )
        output[tag] = f"{ROOT_URLS[category]}/{personal_touch}-{uid}"
    response = {
        "statusCode": 200,
        "body": json.dumps({'links': output})
    }
    return response