import json
import boto3
import os
import requests
import qrcode
from PIL import Image, ImageDraw, ImageFont

BUCKET = os.environ['BUCKET']
API_KEY = os.environ['AIRTABLE_API_KEY']
s3 = boto3.client('s3')
dimentions = (800, 220)
offset = (10, 10)
color = (0, 0, 0)
font = ImageFont.truetype("./qrcodes/arial.ttf", 43)


def update_airtable(record_id, qr_link):
    r = requests.patch(
        'https://api.airtable.com/v0/appPz68CWiJzxnZKj/Designer',
        headers={
            "Authorization": API_KEY,
            "Content-Type": "application/json"
        },
        data=json.dumps({
            "records": [
                {
                    "id": record_id,
                    "fields":
                    {
                        "Label": [{"url": qr_link}]
                    }
                }
            ]
        })
    )

    if r.status_code != 200:
        raise Exception(r)


def make_qr_code(product_code):
    group = product_code.split('-')[2]
    white_background = Image.new("RGB", dimentions, (255, 255, 255))
    code_img = qrcode.make(
        f"https://int.basementremodeling.com/products/get/{product_code}")
    resized_code_img = code_img.resize(
        (round(code_img.size[0]*0.5), round(code_img.size[1]*0.5)))
    white_background.paste(resized_code_img, offset)
    draw = ImageDraw.Draw(white_background)
    draw.text((300, 25), f"Stacked Stone", color, font=font)
    draw.text((300, 85), f"Group: {group}", color, font=font)
    draw.text((300, 145), f"SKU: {product_code}", color, font=font)
    white_background.save(f"/tmp/{product_code}.png")

    s3.upload_file(f"/tmp/{product_code}.png", BUCKET,
                   f"products/{product_code}/label.png", ExtraArgs={"ACL": "public-read"})
    return f"https://{BUCKET}.s3.amazonaws.com/products/{product_code}/label.png"


def handler(event, context):
    body = event['body']
    if os.environ.get('IS_LOCAL') is None:
        body = json.loads(body)
    qr_link = make_qr_code(body['sku'])
    print(qr_link)
    update_airtable(body['id'], qr_link)
    return {
        "statusCode": 200
    }
