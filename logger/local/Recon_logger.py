#!/usr/bin/env python3
import obd
from datetime import datetime,timezone
from obd.commands import __mode1__ as cmdlist
import concurrent.futures 
#from pprint import pprint
#from decimal import Decimal
from setup import Database

class Logger(Database):
    def __init__(self,path) -> None:
        #silence debug messgages
        obd.logger.removeHandler(obd.console_handler)
        #create connection to elm interface
        self.connect=obd.OBD(path)
        #Check for connection
        if(self.connect):
            print("\nConnected to ELM Interface.")
        else:
            print("\nUnable to connect, Please check your connection:(")
    
    def logger(self):
        with concurrent.futures.ProcessPoolExecutor(200) as executor:
            executor.map(self.get_metrics,cmdlist,chunksize=500)
    
    def get_metrics(self,cmd,database=Database().database):
        data={"metric_name":"","time_stamp":0,"value":""}
        if(self.connect.supports(cmd)):
            response=self.connect.query(cmd)
            data["metric_name"]=cmd.desc
            data["time_stamp"]=int(round(datetime.now(timezone.utc).timestamp()))
            #data["time_stamp"]=Decimal(datetime.now(timezone.utc).timestamp())
            data["value"]=str(response.value)

            #Add collected data to database instance
            database.add_metric(data["metric_name"],data["time_stamp"],data["value"])


if __name__=="__main__":
    recon_event=Logger("/dev/pts/3")
    #Ensure connection
    while(recon_event.connect.is_connected()):
        recon_event.logger()
        
