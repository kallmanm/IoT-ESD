from ..sensors import sps30

device_port = "/dev/ttyUSB0"

sensor_sps30 = sps30.Sps30(device_port)
print(f'Sps30 activated: {sensor_sps30.ser.is_open}')

sensor_sps30.start_measurement()
data_readout = sensor_sps30.read_measured_values()
print(f'{data_readout}')

sensor_sps30.stop_measurement()

sensor_sps30.close_port()
print(f'Is port open: {sensor_sps30.ser.is_open}')
print(f'Should be False')
sensor_sps30.open_port()
print(f'Is port open: {sensor_sps30.ser.is_open}')
print(f'Should be True')
sensor_sps30.close_port()
exit()
