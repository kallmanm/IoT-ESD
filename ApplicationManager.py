# IMPORTS
from SensorManager import Sensor
import time
import os
import json


# CODE
class AppManager:
    def __init__(self, config):
        self.config = config

    sensor = Sensor()

    # Data management functions related to IoT Manager
    def connect_to_iot_manager(self):
        pass
