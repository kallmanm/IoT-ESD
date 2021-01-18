"""
Test script for Sps30 class testing that baseline class functionality is working.
"""
from sensors import sps30
import time

device_port = "/dev/ttyUSB0"

# 1. Test __init__()
print(f'----------')
print(f'1. Test __init__()\n\n')
sensor_sps30 = sps30.Sps30(device_port, debug=True)
print(f'Sps30 activated: {sensor_sps30.ser.is_open}')
print(f'\n\n')
ress = sensor_sps30.device_information()
print(ress)
ress =sensor_sps30.device_information(return_info='serial_number')
print(ress)

# 2. Test start_measurement() default mode -> float values
# start_up_time recommended values depending on particle air values: 8,16 or 30 seconds.
print(f'----------')
print(f'2. Test start_measurement() default mode -> float values')
sensor_sps30.start_measurement(start_up_time=8)
print(f'\n\n')

# 3. Test read_measured_values() default mode -> float values
print(f'----------')
print(f'3. Test read_measured_values() default mode -> float values')
for i in range(2):
    data_readout = sensor_sps30.read_measured_values()
    print(f'data output number {i}: {data_readout}')
    time.sleep(1)
print(f'\n\n')

# 4. Test stop_measurement()
print(f'----------')
print(f'4. Test stop_measurement()')
sensor_sps30.stop_measurement()
print(f'\n\n')

# 5. Test close_port()
print(f'----------')
print(f'5. Test open_port()')
sensor_sps30.close_port()
print(f'Is port open: {sensor_sps30.ser.is_open}')
print(f'Should be False')
print(f'\n\n')
exit()
