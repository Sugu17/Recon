from dynamodb_api import DynamoDB
import logging
import boto3
import sys
class Database:
    def __init__(self) -> None:
        #setup database
        self.set_up_db("Default")

    def set_up_db(self,table_name):
        logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
        #Instantiate database object
        self.database=DynamoDB(boto3.resource("dynamodb",endpoint_url="http://localhost:8000"))
        #Check for existing table
        self.table_exists=self.database.exists(table_name)
        if not self.table_exists:
            print(f"\nCreating new table with name {table_name}")
            self.database.create_table(table_name)
        else:
            print(f"\nTable '{table_name}' exists.")

if __name__=="__main__":
    try:
        database=Database()
    except KeyboardInterrupt:
        sys.exit()
        #emulator.database.delete_table
        


