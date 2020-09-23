from SensorManager import Sensor
import time
import os
import json


# The idea is that the AppManager is instantiated and creates
# an instance of the SensorManger class Sensor. The Sensor class
# in its own turn instantiates the bridge class and the right sensors classes.
class AppManager:
    def __init__(self, config):
        self.config = config

    sensor = Sensor()

    # Data management functions related to IoT Manager
    def connect_to_iot_manager(self):
        pass

    def iot_listener(self):
        pass

    def validate_instructions(self):
        pass
