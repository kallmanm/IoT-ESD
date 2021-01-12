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
    def __init__(self, sensor_info, sensors, actions):
        self.sensor_info = sensor_info
        self.activate_sensors(sensors)
        self.actions = actions

    def activate_sensors(self, sensor_list):
        # activate sensor classes
        if 'sps30' in sensor_list:
            sensor_sps30 = sps30.Sps30(self.sensor_info)
        if 'scd30' in sensor_list:
            # sensor_scd30
            pass
        if 'sps30' in sensor_list:
            # sensor_svm30
            pass

    def process_actions(self, action_list):
        for action in action_list:
            # do actions
            pass
        pass


# sensor_sps30 = sps30.Sps30(device_port)
# sensor_sps30.start_measurement()
# data_readout = sensor_sps30.read_measured_values()
# print(f'{data_readout}')
# sensor_sps30.stop_measurement()
# sensor_sps30.close_port()
# exit()
