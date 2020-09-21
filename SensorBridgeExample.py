# Source Code: https://sensirion.github.io/python-i2c-svm40/quickstart.html


import time
from sensirion_shdlc_driver import ShdlcSerialPort, ShdlcConnection
from sensirion_shdlc_sensorbridge import SensorBridgePort, \
    SensorBridgeShdlcDevice, SensorBridgeI2cProxy
from sensirion_i2c_driver import I2cConnection
from sensirion_i2c_svm40 import Svm40I2cDevice

# Connect to the SensorBridge with default settings:
#  - baudrate:      460800
#  - slave address: 0
with ShdlcSerialPort(port='COM1', baudrate=460800) as port:
    bridge = SensorBridgeShdlcDevice(ShdlcConnection(port), slave_address=0)
    print("SensorBridge SN: {}".format(bridge.get_serial_number()))

    # Configure SensorBridge port 1 for SVM40
    bridge.set_i2c_frequency(SensorBridgePort.ONE, frequency=100e3)
    bridge.set_supply_voltage(SensorBridgePort.ONE, voltage=3.3)
    bridge.switch_supply_on(SensorBridgePort.ONE)

    # Create SVM40 device
    i2c_transceiver = SensorBridgeI2cProxy(bridge, port=SensorBridgePort.ONE)
    device = Svm40I2cDevice(I2cConnection(i2c_transceiver))

    # Print some device information
    print("Version: {}".format(device.get_version()))
    print("Serial Number: {}".format(device.get_serial_number()))

    # Start measurement
    device.start_measurement()
    print("Measurement started... ")
    while True:
        time.sleep(10.)
        air_quality, humidity, temperature = device.read_measured_values()
        # use default formatting for printing output:
        print("{}, {}, {}".format(air_quality, humidity, temperature))