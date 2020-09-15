import time
import yaml
from sensirion_shdlc_driver import ShdlcSerialPort, ShdlcConnection
from sensirion_shdlc_sensorbridge import SensorBridgePort, \
    SensorBridgeShdlcDevice, SensorBridgeI2cProxy
from sensirion_i2c_driver import I2cConnection
from sensirion_i2c_svm40 import Svm40I2cDevice

#with open('sensors.yaml') as f:
#    data = yaml.load(f, Loader=yaml.FullLoader)
#    print(data)

class Sensor:
    power = 'off'

    def __init__(self, config):
        self.config

    def check_sensor_status(self):
        return True

    def power_on(self):
        power = 'on'
        print(f'The power is {power}')
        # run functionality to turn on sensor if needed.

    def power_off(self):
        power = 'off'
        print(f'The power is {power}')
        # run functionality to turn off sensor if needed.

    def collect_data(self):
        try:
            if self.check_sensor_status():
                pass

        except RuntimeError as e:
            print(f'{e}')
