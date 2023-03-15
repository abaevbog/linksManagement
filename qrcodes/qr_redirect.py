import os
import json
import requests



def airtable_path_url(id):
    return f"https://basementremodelingcom.retool.com/embedded/public/2fad58a9-af7a-40fc-8d2a-5961ef379605#uid={id}"

table_paths = {'showroom' : {'airtable_path' : 'applY1S3QaNjNFQgX/Showroom', 'to_url' : airtable_path_url}}

def handler(event, context):
    key = event["pathParameters"]['code'].replace('/','')
    table = event["pathParameters"]['table'].replace('/','')

    airtable_path = table_paths[table]['airtable_path']
    to_url = table_paths[table]['to_url'](key)

    return {
            "statusCode": 301,
            "headers": {'Location': f"{to_url}"}
        }