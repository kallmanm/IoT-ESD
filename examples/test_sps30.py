"""
Test script for Sps30 class testing all class functionality is working.
"""
from ..sensors import sps30

device_port = "/dev/ttyUSB0"

# 1. Tests __init__()
sensor_sps30 = sps30.Sps30(device_port, debug=True)
print(f'Sps30 activated: {sensor_sps30.ser.is_open}')

# 2. Tests start_measurement()
sensor_sps30.start_measurement()

# 3. Tests read_measured_values()
# TODO: add tests for both modes: float and integer
for i in range(5):
    data_readout = sensor_sps30.read_measured_values()
    print(f'data output number {i}: {data_readout}')

# 4. Tests stop_measurement()
sensor_sps30.stop_measurement()

# 5. Tests close_port()
sensor_sps30.close_port()
print(f'Is port open: {sensor_sps30.ser.is_open}')
print(f'Should be False')

# 6. Tests open_port()
sensor_sps30.open_port()
print(f'Is port open: {sensor_sps30.ser.is_open}')
print(f'Should be True')
# 7. Re-tests read_measured_values() with reopened port
data_readout = sensor_sps30.read_measured_values()
print(f'data output: {data_readout}')

# Ends test script
sensor_sps30.close_port()
exit()
