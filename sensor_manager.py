from sensors import sps30
import argparse

# with open('sensors.yaml') as f:
#    data = yaml.load(f, Loader=yaml.FullLoader)
#    sensor_bridge_spec = data["sensor-bridge"]
#    svm30_spec = data["sensors"]["svm30"]
#    scd30_spec = data["sensors"]["scd30"]
#    print(svm30_spec)
#    print(scd30_spec)
device_port = "/dev/ttyUSB0"


class SensorManager:
    def __init__(self, sensors_list, action_list):
        if 'sps30' in sensors_list:
            # TODO: add try/except to sensor initiation.
            self.sensor_sps30 = sps30.Sps30(sensors_list['sps30'])
        self.action_list = action_list
        self.listen()

    def listen(self):
        # do actions if activated
        # Maybe use Python IPC
        # https://docs.python.org/3.7/library/ipc.html
        pass

