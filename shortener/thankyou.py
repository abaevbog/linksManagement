import json


def main(event,context):
    with open('Thank_You!.htm','r') as f:
        page = f.read()

    return {
        "statusCode":200,
        "headers": {
            'Content-Type': 'text/html',
        },
        "body":page
    }

