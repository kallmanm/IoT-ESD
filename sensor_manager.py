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
    def __init__(self, config, sensors_list, action_list):
        self.config = config
        if 'sps30' in sensors_list:
            self.sensor_sps30 = sps30.Sps30(self.config)
        self.action_list = action_list
        self.process_actions(self.action_list)
        self.listen()

    def process_actions(self, action_list):
        for action in action_list:
            # do actions
            pass
        pass

    def listen(self):
        # do actions if activated
        pass

# sensor_sps30 = sps30.Sps30(device_port)
# sensor_sps30.start_measurement()
# data_readout = sensor_sps30.read_measured_values()
# print(f'{data_readout}')
# sensor_sps30.stop_measurement()
# sensor_sps30.close_port()
# exit()
