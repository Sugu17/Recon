import os,sys
import random
from Recon_API import Recon_API
import json


class Dashboard():
    def __init__(self) -> None:
        self.api = Recon_API()
        self.engine_sensors = ["Calculated Engine Load", "Engine Coolant Temperature",
                               "Short Term Fuel Trim - Bank 1", "Long Term Fuel Trim - Bank 1", "Intake Manifold Pressure",
                               "Engine RPM", "Air Flow Rate (MAF)", "Throttle Position", "Intake Air Temp", "Engine Run Time",
                               "Absolute load value", "Misfire Monitor General Data"]

        self.exhaust_sensors = ["Secondary Air Status", "Commanded Evaporative Purge", "Evaporative system vapor pressure",
                                "Catalyst Temperature: Bank 1 - Sensor 1", "Absolute Evap system Vapor Pressure", "Evap system vapor pressure",
                                "Catalyst Monitor Bank 1", "EGR Monitor Bank 1", "EVAP Monitor (Cap Off / 0.150\")", "EVAP Monitor (0.090\")",
                                "Purge Flow Monitor", "Heated Catalyst Monitor Bank 1", "Secondary Air Monitor 1", "NOx Absorber Monitor Bank 1",
                                "NOx Catalyst Monitor Bank 1", "PM Filter Monitor Bank 1", "Designed emission requirements"]

        self.fuel_sensors = ["Fuel System Status", "Fuel Pressure", "Intake Air Temp","O2 Sensors Present",
                             "Fuel Rail Pressure (relative to vacuum)", "Fuel Rail Pressure (direct inject)", "Commanded equivalence ratio", "Commanded throttle actuator",
                             "Ethanol Fuel Percent", "Fuel Type", "Fuel rail pressure (absolute)", "Fuel injection timing", "Engine fuel rate", "Fuel System Monitor Bank 1",
                             "Boost Pressure Control Monitor Bank 1"]

        self.oil_sensors = ["Engine oil temperature",
                            "Engine Coolant Temperature"]

        self.battery_sensors = ["Hybrid battery pack remaining life", "Battery - Pack - Capacity kWh estimated 2019+", "Battery - Pack - State of Charge Displayed",
                                "Battery - Pack - State of Charge Variation", "Battery - Thermal Conditioning Inactive Time", "Battery - Heater - Measured W", "Battery - Coolant Temp",
                                "Battery - Module Temp - 1", "Battery - Module Temp - 2", "Battery - Module Temp - 3", "Battery - Module Temp - 4", "Battery - Module Temp - 5", "Battery - Module Temp - 6",
                                "Battery - Module Temp - Max Temp", "Battery - Module Temp - Min Temp", "Battery - Module Temp - Avg Temp", "Battery - Cell - Minimum Voltage", "Battery - Cell - Minimum #",
                                "Battery - Cell - Maximum Voltage", "Battery - Cell - Average Voltage", "Battery - Pack - Resistance", "Battery - Pack - Minimum Voltage",
                                "Battery - Pack - Maximum Voltage", "Battery - Pack - Coolant Level Switch"]

        self.charger_sensors = ["Charger AC Current", "Charger AC Voltage", "Charger HV Current", "Charger HV Voltage", "Charger DC Port Current", "Charger DC Port KW", "Charger DC Port Temperature", "Charger Charging Level",
                                "Charger System Active", "Charger AC Input Status Duty Cycle", "Charger DC Output Status Duty Cycle", "Charger System Inactive Time", "Charger Total Power Output Available", "Charger Power Output Available", "Charger Battery Charger Power Input Available",
                                "Charger System Efficiency (Alt Calc)", "Charger System Efficiency (Active Test Status)", "Charger System Efficiency (Active Test)", "Charger System Efficiency (Passive Test)", "Charger System HV Interlock Circuit Status", "Charger Charging Limit"]

        self.battery_invertor_sensors = ["HV Inverter Voltage LD", "HV Crash Event Lockout", "HV System Interlock Circuit Status", "HV Current", "HV Inverter Voltage HD",
                                         "HV Circuit (HPCM)"]

        self.cabin_sensors = ["Cabin - AC - High Side Sensor Pressure", "Cabin - AC - High Side Sensor Voltage", "Cabin - AC - Low Side Sensor Pressure", "Cabin - AC - Low Side Sensor Voltage", "Cabin - AC - Compressor Speed",
                              "Cabin - AC - Compressor Power Consumption", "Cabin - Blower Motor Speed Request", "Cabin - Climate Control Target Temp Broken", "Cabin - Heater - Measured W",
                              "Cabin - Heater - Coolant Control Solenoid Valve Feed", "Electronics coolant temp", "Electronics coolant pump speed"]

        self.motor_sensors = ["Motor inverter active", "Motor inverter temperature sensor 1", "Motor inverter temperature sensor 2", "Motor inverter temperature sensor 3",
                              "Motor temperature", "Motor speed", "Motor torque", "Axle torque - Measured"]

    def get_data(self, metric):
        request = {}
        request[":metric_name"] = metric
        request[":start"] = 1658034890
        request[":end"] = 1658034950
        response = self.api.query(request)
        temp = json.loads(response.content)["Items"]
        if temp!=[]:
            value=temp[random.randrange(0,len(temp)-1)]["value"]
            print("{:<40}:\t{:<40}".format(metric,value))
        #else:
        #   value="''"
        #   print("{:<40}:\t{:<40}".format(metric,value))

    def print_metrics(self):
        try:
            print("\n[Battery]")
            for data in self.battery_sensors:
                self.get_data(data)
            print("\n[Battery Invertor]")
            for data in self.battery_invertor_sensors:
                self.get_data(data)
            print("\n[Charger]")
            for data in self.charger_sensors:
                self.get_data(data)
            print("\n[Motor]")
            for data in self.motor_sensors:
                self.get_data(data)
            print("\n[Cabin]")
            for data in self.cabin_sensors:
                self.get_data(data)
            print("\n[Engine]")
            for data in self.engine_sensors:
                self.get_data(data)
            print("\n[Fuel]")
            for data in self.fuel_sensors:
                self.get_data(data)
            print("\n[Exhaust]")
            for data in self.exhaust_sensors:
                self.get_data(data)
            print("\n[Oil and Coolant]")
            for data in self.oil_sensors:
                self.get_data(data)

        except KeyboardInterrupt:
            print("\nStopped by interrupt")
            sys.exit()


if __name__ == "__main__":
    event = Dashboard()
    while True:
        os.system("clear")
        event.print_metrics()
