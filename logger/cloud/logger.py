from datetime import datetime, timezone
import obd
from obd.commands import __mode1__ as cmdlist
from Recon_API import Recon_API
from concurrent.futures import ProcessPoolExecutor
from pprint import pprint


class Recon:
    def __init__(self) -> None:
        self.api = Recon_API()
        self.setup_elm()

    def setup_elm(self):
        # silence debug messgages
        obd.logger.removeHandler(obd.console_handler)
        # create connection to elm interface
        path = "/dev/pts/3"
        self.connect = obd.OBD(path)
        # Check for connection
        if(self.connect):
            print("\nConnected to ELM Interface.")
        else:
            print("\nUnable to connect, Please check your connection:(")

    def logger(self):
        with ProcessPoolExecutor() as executor:
            executor.map(self.get_metrics, cmdlist, chunksize=4)

    def get_metrics(self, cmd):
        data = {}
        if(self.connect.supports(cmd)):
            response = self.connect.query(cmd)
            data["metric_name"] = cmd.desc
            data["time_stamp"] = int(
                round(datetime.now(timezone.utc).timestamp()))
            # data["time_stamp"]=Decimal(datetime.now(timezone.utc).timestamp())
            data["value"] = str(response.value)
            # log collected data to database instance
            self.api.post(data)


if __name__ == "__main__":
    event = Recon()
    while event.connect.is_connected():
        event.logger()
