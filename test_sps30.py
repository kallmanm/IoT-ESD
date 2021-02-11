"""
Test script for Sps30 class testing that all class functionality is working.
"""
from sensors import sps30
import time

device_port = "/dev/ttyUSB0"
COUNT = 20
print(f'Device port set to: {device_port}\n')

print(f'******************')

sensor_sps30 = sps30.Sps30(device_port)

print(f'Sps30 __init__(): {sensor_sps30.ser.is_open}\n')

print(f'----------')
print('Device information - product type:')
dipt = sensor_sps30.device_information()
print(dipt)


print(f'----------')
print(f'Testing close_port()')
sensor_sps30.close_port()
print(f'Port Status: {sensor_sps30.ser.is_open}')
print(f'Should be False\n')

print(f'----------')
print(f'Testing open_port()')
sensor_sps30.open_port()
print(f'Port Status: {sensor_sps30.ser.is_open}')
print(f'Should be True\n')


print(f'----------')
print('Device information - serial number:')
di2 = sensor_sps30.device_information(return_info='serial_number')
print(f'{di2}\n')
print(f'******************')


# FLOAT MODE
print(f'******************')
# Test start_measurement() default mode -> float values
# start_up_time recommended values depending on particle air values: 8,16 or 30 seconds.
print(f'----------')
print(f'Test start_measurement() default mode -> float values')
sensor_sps30.start_measurement(start_up_time=8)
print()

# Test read_measured_values() default mode -> float values
print(f'----------')
print(f'Test read_measured_values() default mode -> float values')
for i in range(COUNT):
    data_readout = sensor_sps30.read_measured_values()
    print(f'data output number {i+1}: {data_readout}')
    print()
    time.sleep(1)
print()

# Test stop_measurement()
print(f'----------')
print(f'Test stop_measurement()')
sensor_sps30.stop_measurement()

# INTEGER MODE
print(f'******************')

# Test start_measurement() mode -> integer values
print(f'----------')
print(f'Test start_measurement() default mode -> integer values')
sensor_sps30.start_measurement(mode='integer', start_up_time=8)
print()

# Test read_measured_values() mode -> integer values
print(f'----------')
print(f'Test read_measured_values() default mode -> integer values')
for i in range(COUNT):
    data_readout = sensor_sps30.read_measured_values(mode='integer')
    print(f'data output number {i}: {data_readout}')
    time.sleep(1)
print()

# Test stop_measurement()
print(f'----------')
print(f'Test stop_measurement()')
sensor_sps30.stop_measurement()

print(f'******************')
# Sleep -> Wake up -> Start fan cleaning
sleep = sensor_sps30.sleep()
print(f'sleep - {sleep}')
print('sleeping 4 seconds...')
time.sleep(4)
wk = sensor_sps30.wake_up()
print(f'wake_up - {wk}')


sensor_sps30.start_measurement()
sfc = sensor_sps30.start_fan_cleaning()
print(f'start_fan_clean - {sfc}')
print('sleeping 7 seconds...')
time.sleep(7)
sensor_sps30.stop_measurement()

print(f'******************')
rd = sensor_sps30.read_version()
print(f'read_version - {rd}')
dr = sensor_sps30.device_reset()
print(f'device_reset - {dr}')

print(f'******************')
sensor_sps30.start_measurement(start_up_time=8)
rdsr = sensor_sps30.read_device_status_register()
print(f'{rdsr}')
print('sleeping 3 seconds...')
time.sleep(3)
sensor_sps30.stop_measurement()

sensor_sps30.close_port()
exit()
