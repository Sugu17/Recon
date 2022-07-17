from data import data as sensors_list
import random

class Emulator:
    def get_metrics(self,name):
        data=next((item for item in sensors_list if item["name"]==name),None)
        print(self.gen_value(data))

    def gen_value(self,data:dict):
        temp={}
        temp["metric_name"]=data["name"]
        value=random.randrange(data["min_value"],data["max_value"])
        temp["value"]=str(value)+""+data["unit"]
        return temp

if __name__=="__main__":
    emulator=Emulator()
    emulator.get_metrics("Motor speed")