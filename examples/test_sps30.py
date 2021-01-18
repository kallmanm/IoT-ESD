"""
Test script for Sps30 class testing all class functionality is working.
"""
from ..sensors import sps30

device_port = "/dev/ttyUSB0"

# 1. Tests __init__()
print(f'----------')
print(f'1. Test __init__()\n\n')
sensor_sps30 = sps30.Sps30(device_port, debug=True)
print(f'Sps30 activated: {sensor_sps30.ser.is_open}')
print(f'\n\n')

# 2. Tests start_measurement() default mode -> float values
# start_up_time recommended values depending on particle air values: 8,16 or 30 seconds.
print(f'----------')
print(f'2. Tests start_measurement() default mode -> float values')
sensor_sps30.start_measurement(start_up_time=16)
print(f'\n\n')

# 3. Tests read_measured_values() default mode -> float values
# TODO: add tests for integer mode
print(f'----------')
print(f'3. Tests read_measured_values() default mode -> float values')
for i in range(5):
    data_readout = sensor_sps30.read_measured_values()
    print(f'data output number {i}: {data_readout}')
print(f'\n\n')

# 4. Tests stop_measurement()
print(f'----------')
print(f'4. Tests stop_measurement()')
sensor_sps30.stop_measurement()
print(f'\n\n')

# 5. Tests close_port()
print(f'----------')
print(f'Tests close_port()')
sensor_sps30.close_port()
print(f'Is port open: {sensor_sps30.ser.is_open}')
print(f'Should be False')
print(f'\n\n')

# 6. Tests open_port()
print(f'----------')
print(f'6. Tests open_port()')
sensor_sps30.open_port()
print(f'Is port open: {sensor_sps30.ser.is_open}')
print(f'Should be True')
print(f'\n\n')

# 7. Re-tests read_measured_values() with reopened port
print(f'----------')
print(f'7. Re-tests read_measured_values() with reopened port')
data_readout = sensor_sps30.read_measured_values()
print(f'data output: {data_readout}')
print(f'\n\n')

# Ends test script
sensor_sps30.close_port()
exit()
