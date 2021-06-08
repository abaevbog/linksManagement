import json
import requests
from jinja2 import Environment, FileSystemLoader

def main(event,context):
    try:
        params = event.get('queryStringParameters')
        if params is None:
            params = {}
        url = params.get('url')
        print(params)
        message_parameter = params.get('message')
        if url is not None:
            del params['url']
            x = requests.post(url, data=params)     
    finally:
        env = Environment(loader=FileSystemLoader('./shortener'), trim_blocks=True, lstrip_blocks=True)
        template = env.get_template(f"ThankYou.html")
        page = template.render({'message':message_parameter})

    return {
        "statusCode":200,
        "headers": {
            'Content-Type': 'text/html',
        },
        "body":page
    }

