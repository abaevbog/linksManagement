import json
import os
from jinja2 import Environment, FileSystemLoader
import requests
import ast
import traceback
import urllib


API_KEY = os.environ['AIRTABLE_API_KEY']

def handler(event,context):
    try:
        trade = event["queryStringParameters"].get('trade')
        
        r = requests.get(
            "https://api.airtable.com/v0/appiScywNMqBk3x9e/Directory",
        params= urllib.parse.urlencode({
            'maxRecords' : '100',
            'view' : "Vendors_Service_Area",
            "filterByFormula" : f"FIND('{trade}', {'{Division and Trade}'})",
            "fields[0]" : "Full Name", 
            "fields[1]" : "Zip Codes Serviced",
            "fields[2]" : "Category",
            "fields[3]" : "Division and Trade",
        },quote_via=urllib.parse.quote),
        headers={
            "Authorization": API_KEY
        })
        
        result = json.loads(r.content)
        
        env = Environment(loader=FileSystemLoader('./vendors'), trim_blocks=True, lstrip_blocks=True)
        template = env.get_template(f"zips.html")
        page = template.render(data= result)
    except Exception as e:
        print("Error!!")
        print(e)
        traceback.print_exc() 
        page = "<html>Error. Something broke, please yell at bogdan.</html>" 
    finally:
        return {
                "statusCode":200,
                "headers": {'Content-Type': 'text/html'},
                "body":page
                }