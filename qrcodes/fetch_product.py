import json
import boto3
import os
from jinja2 import Environment, FileSystemLoader
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('qrCodes')


def handler(event,context):
    try:
        key = event["pathParameters"]['code'].replace('/','')
        response = table.get_item(
        Key={
            'productId': key,
            }
        )
        result = response['Item']
        env = Environment(loader=FileSystemLoader('./qrcodes'), trim_blocks=True, lstrip_blocks=True)
        template = env.get_template(f"product_page.html")
        page = template.render()
    except KeyError as e:
        print("Error!")
        print(e)
        env = Environment(loader=FileSystemLoader('./qrcodes'), trim_blocks=True, lstrip_blocks=True)
        template = env.get_template(f"product_page.html")
        page = template.render()    
    finally:
        return {
                "statusCode":200,
                "headers": {'Content-Type': 'text/html'},
                "body":page
                }