from os import sep
from pprint import pprint
import requests
import json

url = "https://2u0rw4lj67.execute-api.ap-south-1.amazonaws.com/Recon/dynamodbmanager"
request = {
    "operation": "query",
    "tableName": "Recon_Database",
    "payload": {
        "ExpressionAttributeValues": {
            ":metric_name": "Calculated Engine Load",
            ":start": 1657600197,
            ":end": 1657600213
        },
        "KeyConditionExpression": "#metric_name = :metric_name and (#time_stamp between :start and :end)",
        "ProjectionExpression": "#value",
        "ExpressionAttributeNames": {
            "#metric_name": "metric_name",
            "#time_stamp": "time_stamp",
            '#value' : "value"
        },
    }
}
print("\nScanning between timestamps 1657039467 and 1657039493\n")
response = requests.post(url, json.dumps(request))
output = json.loads(response.text)

for key, value in output.items():
    if type(value) != list:
        print(f"{key} : {value}")
    else:
        pprint(key)
        for data in value:
            print()
            pprint(data, depth=1)
