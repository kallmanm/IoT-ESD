# Source Code: https://sensirion.github.io/python-i2c-svm40/quickstart.html


import time
import yaml
from sensirion_shdlc_driver import ShdlcSerialPort, ShdlcConnection
from sensirion_shdlc_sensorbridge import SensorBridgePort, \
    SensorBridgeShdlcDevice, SensorBridgeI2cProxy
from sensirion_i2c_driver import I2cConnection
from sensirion_i2c_svm40 import Svm40I2cDevice

with open('sensors.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    sensor_bridge_spec = data["sensor-bridge"]
    svm30_spec = data["sensors"]["svm30"]
    scd30_spec = data["sensors"]["scd30"]

# Connect to the SensorBridge with default settings:
#  - baudrate:      460800
#  - slave address: 0
with ShdlcSerialPort(port=sensor_bridge_spec["port"],
                     baudrate=sensor_bridge_spec["baudrate"]) as port:
    bridge = SensorBridgeShdlcDevice(ShdlcConnection(port),
                                     slave_address=sensor_bridge_spec["slave_address"])
    print("SensorBridge SN: {}".format(bridge.get_serial_number()))

    # Configure SensorBridge port 1 for SVM40, in our case we are testing svm30.
    bridge.set_i2c_frequency(SensorBridgePort.TWO,
                             frequency=svm30_spec["frequency"])
    bridge.set_supply_voltage(SensorBridgePort.TWO,
                              voltage=svm30_spec["voltage"])
    bridge.switch_supply_on(SensorBridgePort.TWO)

    # Create SVM40 device
    i2c_transceiver = SensorBridgeI2cProxy(bridge, port=SensorBridgePort.ONE)
    device = Svm40I2cDevice(I2cConnection(i2c_transceiver))

    # Print some device information
    # print("Version: {}".format(device.get_version()))
    # print("Serial Number: {}".format(device.get_serial_number()))

    # Start measurement
    #device.start_measurement()
    #print("Measurement started... ")
    #e = 1
    #while e < 4:
    #    time.sleep(10.)
    #    air_quality, humidity, temperature = device.read_measured_values()
    #    # use default formatting for printing output:
    #    print("{}, {}, {}".format(air_quality, humidity, temperature))
    #    e += 1
    #device.stop_measurement()
    bridge.switch_supply_off(SensorBridgePort.TWO)

exit()
