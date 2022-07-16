from urllib import response
import requests,json
from pprint import pprint
data = {
    "operation": "create",
    "tableName": "Recon_Database",
    "payload": {
        "Item": {
            "metric_name": "Battery Temperature",
            "time_stamp": 760008,
            "value": "42C"
        }
    }
}
response=requests.put("https://2u0rw4lj67.execute-api.ap-south-1.amazonaws.com/Recon/dynamodbmanager",json.dumps(data))
if response.status_code==200:
    print("Logging successfull.")
    pprint(response)
