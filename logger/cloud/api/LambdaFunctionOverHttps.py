from __future__ import print_function
import boto3
from botocore.exceptions import ClientError
import json
import logging

logger=logging.getLogger(__name__)

def create_table(database):
    try:
        dynamo=database.create_table(
                TableName="Recon_Database",
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
        dynamo.wait_until_exist()
        return dynamo
    except ClientError as error:
        logger.error(
            "Couldn't create table %s. Here's why: %s: %s", "Recon_Database",
            error.response['Error']['Code'], error.response['Error']['Message'])
        raise

print('Loading function')
def handler(event, context):
    '''Provide an event that contains the following keys:
      - operation: one of the operations in the operations dict below
      - tableName: required for operations that interact with DynamoDB
      - payload: a parameter to pass to the operation being performed
    '''
    print("Received event: " + json.dumps(event, indent=2))
    #Check for table
    database=boto3.resource('dynamodb')
    if 'tableName' in event:
        dynamo = database.Table(event['tableName'])
    else:
        dynamo=create_table(database)
    #Operations done by the API
    operations = {
    'create': lambda x: dynamo.put_item(**x),
    'read': lambda x: dynamo.get_item(**x),
    'update': lambda x: dynamo.update_item(**x),
    'delete': lambda x: dynamo.delete_item(**x),
    'list': lambda x: dynamo.scan(**x),
    'echo': lambda x: x,
    'ping': lambda x: 'ping'}

    operation = event['operation']
    if operation in operations:
        return operations[operation](event.get('payload'))
    else:
        raise ValueError('Unrecognized operation "{}"'.format(operation))