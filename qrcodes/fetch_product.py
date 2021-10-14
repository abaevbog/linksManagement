import json
import boto3
import os
from jinja2 import Environment, FileSystemLoader
import requests
import ast
import traceback
import urllib
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('qrCodes')


def handler(event,context):
    try:
        key = event["pathParameters"]['code'].replace('/','')
        formula = urllib.parse.urlencode({"filterByFormula" : f"SKU = '{key}'"})
        print(formula)
        r = requests.get(
            f"https://api.airtable.com/v0/appPz68CWiJzxnZKj/Designer?maxRecords=1&view=All&{formula}",
        headers={
            "Authorization": "Bearer keyfcdTfG74vVDNCo"
        })
        result = ast.literal_eval(r.content.decode("UTF-8"))['records'][0]['fields']
        env = Environment(loader=FileSystemLoader('./qrcodes'), trim_blocks=True, lstrip_blocks=True)
        template = env.get_template(f"product_page.html")
        page = template.render(data=result)
    except Exception as e:
        print("Error!!")
        print(e)
        traceback.print_exc() 
        page = "<html>Error. Product could not be found.</html>" 
    finally:
        return {
                "statusCode":200,
                "headers": {'Content-Type': 'text/html'},
                "body":page
                }