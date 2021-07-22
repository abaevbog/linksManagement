import json
import boto3
import os
import requests
import qrcode
import io
BUCKET = os.environ['BUCKET']
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
table = dynamodb.Table('qrCodes')

def make_qr_code(product_code):
    img = qrcode.make(f"https://int.basementremodeling.com/products/{product_code}")
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    s3.upload_fileobj(img_byte_arr,BUCKET,f"products/{product_code}/qr_code.png",ExtraArgs={"ACL" : "public-read"})
    return f"https://{BUCKET}.s3.amazonaws.com/products/{product_code}/qr_code.png"

def upload_to_s3(link,name,product_code):
    r = requests.get(link)
    s3.upload_fileobj(io.BytesIO(r.content),BUCKET,f"products/{product_code}/{name}.png", ExtraArgs={"ACL" : "public-read"})
    return f"https://{BUCKET}.s3.amazonaws.com/products/{product_code}/{name}.png"

# body: {'productId' : "string", "productImageUrl" : "string","productSettingUrl" : "string" , "description" : "string", "name" : "string", ...}
def handler(event,context):
    body = event['body']
    if os.environ.get('IS_LOCAL') is None:
        body = json.loads(body)
    # upload two pictures to s3
    productLink = upload_to_s3(body["productImageUrl"],"productImage",body["productId"])
    settingsLink = upload_to_s3(body["productSettingUrl"],"settingImage",body["productId"])
    qr_link = make_qr_code(body['productId'])
    body['qrCode'] = qr_link
    body["productImageUrl"] = productLink
    body["productSettingUrl"] = settingsLink
    # put into to dynamodb
    table.put_item(Item=body)
    response = {
        "statusCode": 200,
        "body": json.dumps({'item_name' : body['name'],'item_code' : body['productId'] ,'qr_code' : qr_link})
    }
    return response