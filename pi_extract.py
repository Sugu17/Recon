import obd
import time
from obd.commands import __mode1__ as cmdlist

#silence debug messgages
obd.logger.removeHandler(obd.console_handler)

#create connection to elm interface
connect=obd.OBD("/dev/pts/3")

#Check for connection
if(connect):
    print("Connected to ELM Interface.")
    #Ensure connection
    while (connect.is_connected()):
        for cmd in cmdlist:
            if(connect.supports(cmd)):
                response=connect.query(cmd)
                print("\n{} : {}".format(cmd.desc,response.value))
                time.sleep(1)
else:
    print("Unable to connect, Please check your connection:(")