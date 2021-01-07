import time
import yaml
from sensirion_shdlc_driver import ShdlcSerialPort, ShdlcConnection
from sensirion_shdlc_sensorbridge import SensorBridgePort, \
    SensorBridgeShdlcDevice, SensorBridgeI2cProxy
from sensirion_i2c_driver import I2cConnection
from sensirion_i2c_svm40 import Svm40I2cDevice


# with open('sensors.yaml') as f:
#    data = yaml.load(f, Loader=yaml.FullLoader)
#    sensor_bridge_spec = data["sensor-bridge"]
#    svm30_spec = data["sensors"]["svm30"]
#    scd30_spec = data["sensors"]["scd30"]
#    print(svm30_spec)
#    print(scd30_spec)


class SensorManager:
    sensor_power = False

    def __init__(self, config):
        self.config = config

    def check_sensor_status(self):
        if self.sensor_power:
            return True
        else:
            return False

    def power_on(self):
        self.sensor_power = True
        print(f'The power is {self.sensor_power}')
        # run functionality to turn on sensor if needed.

    def power_off(self):
        self.sensor_power = False
        print(f'The power is {self.sensor_power}')
        # run functionality to turn off sensor if needed.

    def collect_data(self):
        try:
            if self.check_sensor_status():
                print('random data atm')

        except RuntimeError as e:
            print(f'{e}')
