import os
import json
import requests


def handler(event, context):
    key = event["pathParameters"]['code'].replace('/','')
    try:
        r = requests.get(
            'https://api.airtable.com/v0/applY1S3QaNjNFQgX/Technical%20Guide%20Items',
            headers={
                "Authorization": "Bearer keyfcdTfG74vVDNCo",
                "Content-Type": "application/json"
            },
            params= {
                "fields[]": "Item Id",
                "filterByFormula" : f"UID='{key}'"
            }
        )
        item_id = json.loads(r.content)['records'][0]['fields']['Item Id']
        return {
                    "statusCode": 301,
                    "headers": {'Location': f"https://info.basementremodeling.com/guide_details/{item_id}"}
                }
    except Exception as e:
        return {
            "statusCode": 404,
            "body" : "Item not found"
        }
