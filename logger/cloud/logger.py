from datetime import datetime, timezone
import sys
import time
import obd
from emulator import Emulator
from data import data as sensor_list
from obd.commands import __mode1__, __mode6__
from Recon_API import Recon_API
from concurrent.futures import ProcessPoolExecutor

cmdlist = __mode1__+__mode6__


class Recon:
    def __init__(self) -> None:
        self.api = Recon_API()
        self.setup_elm()
        self.emulator = Emulator()

    def setup_elm(self):
        # silence debug messgages
        obd.logger.removeHandler(obd.console_handler)
        # create connection to elm interface
        path = "/dev/pts/5"
        self.connect = obd.OBD(path)
        # Check for connection
        if(self.connect):
            print("\nConnected to ELM Interface.")
        else:
            print("\nUnable to connect, Please check your connection:(")

    def logger(self):
        try:
            with ProcessPoolExecutor() as executor:
                executor.map(self.post_metrics, sensor_list,
                             chunksize=200)
                executor.map(self.get_metrics, cmdlist,
                             chunksize=100, timeout=0.1)

        except KeyboardInterrupt:
            print("Exiting")
            sys.exit()

    def get_metrics(self, cmd):
        try:
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
        except KeyboardInterrupt:
            print("Exiting...")
            sys.exit()

    def post_metrics(self, temp):
        try:
            data = self.emulator.gen_value(temp)
            data["time_stamp"] = int(
                round(datetime.now(timezone.utc).timestamp()))
            self.api.post(data)
        except KeyboardInterrupt:
            print("Exiting...")


if __name__ == "__main__":
    event = Recon()
    try:
        while event.connect.is_connected():
            time.sleep(0.1)
            event.logger()
    except KeyboardInterrupt:
        sys.exit()
