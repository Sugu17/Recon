from pprint import pprint
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
import logging

logger=logging.getLogger(__name__)

class DynamoDB:

    #Instantiate dynamo db
    def __init__(self,database) -> None:
        self.database=database
        self.table=None 

    #Check for existing db instance
    def exists(self,table_name):
        try:
            table=self.database.Table(table_name)
            table.load()
            db_exists=True
        except ClientError as error:
            if error.response['Error']['Code']=='ResourceNotFoundException':
                db_exists=False
            else:
                logger.error(
                    "Couldn't check for existence of %s. Here's why: %s: %s",
                    table_name,
                    error.response['Error']['Code'],
                    error.response['Error']['Message'])
                raise
        else:
            self.table = table
        return db_exists

    def create_table(self,table_name):
        try:
            self.table=self.database.create_table(
                TableName=table_name,
                KeySchema=[
                    {"AttributeName":"metric_name","KeyType":"HASH"},
                    {"AttributeName":"time_stamp","KeyType":"RANGE"}
                ],
                AttributeDefinitions=[
                    {"AttributeName":"metric_name","AttributeType":'S'},
                    {"AttributeName":"time_stamp","AttributeType":'N'}
                ],
                ProvisionedThroughput={'ReadCapacityUnits': 10, 
                'WriteCapacityUnits': 10})
            self.table.wait_until_exists()
        except ClientError as error:
            logger.error(
                "Couldn't create table %s. Here's why: %s: %s", table_name,
                error.response['Error']['Code'], error.response['Error']['Message'])
            raise
        else:
            return self.table
    
    def write_batch(self,metrics):
        try:
            with self.table.batch_writer() as writer:
                for data in metrics:
                    writer.put_item(Item=data)
        except ClientError as error:
            logger.error(
                "Couldn't load data into table %s. Here's why: %s: %s", 
                self.table.name,
                error.response['Error']['Code'], error.response['Error']['Message'])
            raise
    
    def add_metric(self,metric_name,time_stamp,value):
        try:
            self.table.put_item(
                Item={
                    "metric_name":metric_name,
                    "time_stamp":time_stamp,
                    "value":value
                }
            )
            print(f"\nAdded {metric_name} with timestamp {time_stamp}")
        except ClientError as error:
            logger.error(
                "Couldn't add data %s to table %s. Here's why: %s: %s",
                metric_name, self.table.name,
                error.response['Error']['Code'], error.response['Error']['Message'])
            raise

    def get_metric(self,metric_name,time_stamp):
        try:
            response=self.table.get_item(
                Key={
                    'metric_name':metric_name,
                    'time_stamp':time_stamp
                    })  
        except ClientError as error:
            logger.error(
                "Couldn't get data %s from table %s. Here's why: %s: %s",
                metric_name, self.table.name,
                error.response['Error']['Code'], error.response['Error']['Message'])
            raise
        else:
            return response['Item']
    
    def update_metric(self,metric_name,time_stamp,value):
        try:
            response=self.table.update_item(Key={"metric_name":metric_name,
            "time_stamp":time_stamp},
            UpdateExpression="set value=:v",
            ExpressionAttributeValues={
                ":v":value
            },
            ReturnValues="UPDATED_NEW")
        except ClientError as error:
            logger.error(
                "Couldn't update data %s in table %s. Here's why: %s: %s",
                metric_name, self.table.name,
                error.response['Error']['Code'], error.response['Error']['Message'])
            raise
        else:
            return response['Attributes']
    
    def query_metrics(self,time_stamp):
        try:
            response=self.table.query(
                KeyConditionExpression=Key("time_stamp").eq(time_stamp))
        except ClientError as error:
            logger.error(
                "Couldn't query for datas collected in %s. Here's why: %s: %s", time_stamp,
                error.response['Error']['Code'], error.response['Error']['Message'])
            raise
        else:
            return response['Items']
    
    def scan_metrics(self,time_stamp_range):
        data=[]
        scan_key_args={
                "FilterExpression":Key("time_stamp").between(
                    time_stamp_range['first'],
                    time_stamp_range['second']),
                "ProjectionExpression":"#time, metric_name, value",
                "ExpressionAttributeNames":{"#time":"time_stamp"}
        }
        try:
            done=False
            start_key=None
            while not done:
                if start_key:
                    scan_key_args["ExclusiveStartKey"]=start_key
                response=self.table.scan(**scan_key_args)
                data.extend(response.get("Items",[]))
                start_key=response.get("LastEvaluatedKey",None)
                done=start_key is None
        except ClientError as error:
            logger.error(
                "Couldn't scan for data. Here's why: %s: %s",
                error.response['Error']['Code'], error.response['Error']['Message'])
            raise
        return data
    
    def get_all(self):
        try:
            response=self.table.scan()
            data=response['Items']

            while "LastEvaluatedKey" in response:
                response=self.table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                data.extend(response['Items'])
        except ClientError as error:
            logger.error(
                "Couldn't scan for data. Here's why: %s: %s",
                error.response['Error']['Code'], error.response['Error']['Message'])
            raise
        return data


    def delete_metric(self,metric_name,time_stamp):
        try:
            self.table.delete_item(Key={"metric_name":metric_name,
            "time_stamp":time_stamp})
        except ClientError as error:
            logger.error(
                "Couldn't delete data %s. Here's why: %s: %s", metric_name,
                error.response['Error']['Code'], error.response['Error']['Message'])
            raise
    def delete_table(self):
        try:
            self.table.delete()
            self.table=None
        except:
            logger.error(
                "Couldn't delete table. Here's why: %s: %s",
                error.response['Error']['Code'], error.response['Error']['Message'])
            raise

def test(table_name,database):
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    Database=DynamoDB(database)
    table_exists=Database.exists(table_name)

    if not table_exists:
        print(f"\nCreating table with name {table_name}...")
        Database.create_table(table_name)
        print(f"\nCreated table {Database.table.name}")

    print("Adding metrics to database...")
    Database.add_metric(metric_name="RPM",time_stamp=4000,value="1200 RPM")
    Database.add_metric(metric_name="RPM",time_stamp=4550,value="1800 RPM")
    print("Added data to database.")
    print("Getting data from database...")
    pprint(Database.get_all())

    
if __name__=="__main__":
    try:
        test("Default",boto3.resource("dynamodb",endpoint_url="http://localhost:8000"))
    except Exception as error:
        print(f"Something went wrong with the Code! Here's what: {error}")

        


    


