import obd
#import time
from obd.commands import __mode1__ as cmdlist
import concurrent.futures 

class Logger:
    def __init__(self,path) -> None:
        #silence debug messgages
        obd.logger.removeHandler(obd.console_handler)
        #create connection to elm interface
        self.connect=obd.OBD(path)
    
    def logger(self):
    #Check for connection
        if(self.connect):
            print("Connected to ELM Interface.")
            #Ensure connection
            while (self.connect.is_connected()):
                with concurrent.futures.ProcessPoolExecutor(100) as executor:
                    executor.map(self.get_metrics,cmdlist,chunksize=500)
        else:
            print("Unable to connect, Please check your connection:(")
    
    def get_metrics(self,cmd):
        if(self.connect.supports(cmd)):
            response=self.connect.query(cmd)
            print("\n{} : {}".format(cmd.desc,response.value))
        

if __name__=="__main__":
    recon_event=Logger("/dev/pts/3")
    recon_event.logger()

        
