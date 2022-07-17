import sys
from Recon_API import Recon_API
from concurrent.futures import ProcessPoolExecutor
from emulator import Emulator
from datetime import datetime, timezone

sensor_list= []
class Recon:
    def __init__(self) -> None:
        self.api = Recon_API()
        self.emulator = Emulator()
    def logger(self):
        try:
            with ProcessPoolExecutor() as executor:
                executor.map(self.post_metrics, sensor_list,
                             chunksize=200)
        except KeyboardInterrupt:
            sys.exit()
    def post_metrics(self, temp):
        try:
            data = self.emulator.gen_value(temp)
            data["time_stamp"] = int(
                round(datetime.now(timezone.utc).timestamp()))
            self.api.post(data)
        except KeyboardInterrupt:
            print("Exiting...")

if __name__=="__main__":
    event=Recon()
    while True:
        event.logger()