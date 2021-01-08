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

sensor_sps30 = sps30.Sps30(device_port)
sensor_sps30.start()
sensor_sps30.read()
sensor_sps30.stop()
