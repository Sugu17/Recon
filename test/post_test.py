from pprint import pprint
import requests
import json

url = "https://2u0rw4lj67.execute-api.ap-south-1.amazonaws.com/Recon/dynamodbmanager"
request = {
    "operation": "read",
    "payload": {
        "TableName": "Recon_Database",
        "Key": {
            "metric_name": "Calculated Engine Load",
            "time_stamp": 1657600197
        }
    }
}
response = requests.post(url, json.dumps(request))
pprint(response.content)
