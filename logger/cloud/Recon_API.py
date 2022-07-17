import requests
import json
from pprint import pprint


class Recon_API:
    def __init__(self) -> None:
        self.url = "https://2u0rw4lj67.execute-api.ap-south-1.amazonaws.com/Recon/dynamodbmanager"
        self.data = {
            "operation": "",
            "tableName": "Recon_Database",
            "payload": {

            }
        }

    def success(self, response: requests.Response) -> bool:
        if response.status_code == 200:
            return True
        if response.status_code == 400:
            return False

    def get(self, data: dict):
        self.data['operation'] = "read"
        self.data['payload']['Key'] = data
        payload = json.dumps(self.data)
        response = requests.post(self.url, payload)
        if self.success(response):
            print("Retrieved data from the database")
            # pprint(response.content)
            return response
        else:
            print("\nFailed to read data")
            pprint(response)

    def post(self, data: dict):
        self.data['operation'] = "create"
        self.data['payload']['Item'] = data
        payload = json.dumps(self.data)
        response = requests.post(self.url, payload)
        if self.success(response):
            print(
                f"\nLogged {data['metric_name']} with timestamp {data['time_stamp']}")
        else:
            print("\nFailed to log data")
            pprint(response.content)

    def delete(self, data: dict):
        self.data['operation'] = "delete"
        self.data['payload']['Item'] = data
        payload = json.dumps(self.data)
        response = requests.post(self.url, payload)
        if self.success(response):
            print(
                f"\nRemoved {data['metric_name']} with timestamp {data['time_stamp']}")
        else:
            print("\nFailed to remove data")
            pprint(response.content)

    def list(self):
        self.data['operation'] = "list"
        self.data['payload='] = {}
        payload = json.dumps(self.data)
        response = requests.post(self.url, payload)
        if self.success(response):
            print(response.status_code)
            return response
            # pprint(response.content)
        else:
            print("\nFailed to get data")

    def query(self,data:dict):
        self.data['operation'] = "query"
        self.data['payload']['ExpressionAttributeValues']=data
        self.data['payload'][
        'KeyConditionExpression'] = "#metric_name = :metric_name and (#time_stamp between :start and :end)"
        self.data['payload']['ProjectionExpression'] = "#value"
        self.data['payload']['ExpressionAttributeNames'] = {
            "#metric_name": "metric_name",
            "#time_stamp": "time_stamp",
            '#value': "value"
        }
        payload=json.dumps(self.data)
        response=requests.post(self.url,payload)
        if self.success(response):
            #print(response.status_code)
            return response
        else:
            print("\nFailed to query data")


if __name__ == "__main__":
    api = Recon_API()
    data = {
        "metric_name": "Speed",
        "time_stamp": 3230,
        "value": "3000RPM",
    }
    api.post(data)
