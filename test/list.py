from pprint import pprint
import requests
import json

url = "https://2u0rw4lj67.execute-api.ap-south-1.amazonaws.com/Recon/dynamodbmanager"
request = {
    "operation": "list",
    "tableName": "Recon_Database",
    "payload": {}
}
response = requests.post(url, json.dumps(request))
pprint(response.content)
