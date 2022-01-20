import json
import os
from jinja2 import Environment, FileSystemLoader
import requests
import ast
import traceback
import urllib






r = requests.get(
    "https://api.airtable.com/v0/appiScywNMqBk3x9e/Directory",
params= urllib.parse.urlencode({
    'maxRecords' : '75',
    'view' : "Vendors_Zip_Codes",
    "fields[0]" : "Full Name", 
    "fields[1]" : "Zip Codes Serviced"
},quote_via=urllib.parse.quote),
headers={
    "Authorization": "Bearer keyfcdTfG74vVDNCo"
})
print(r.url)
result = json.loads(r.content)
print(result)
#https://api.airtable.com/v0/appiScywNMqBk3x9e/Directory?maxRecords=75&view=Vendors_Zip_Codes&fields%5B%5D=Full%20Name&fields%5B%5D=Zip%20Codes%20Serviced
#https://api.airtable.com/v0/appiScywNMqBk3x9e/Directory?maxRecords=75&view=Vendors_Zip_Codes&fields%255B%255D=%5B%27Full%20Name%27%2C%20%27Zip%20Codes%20Serviced%27%5D