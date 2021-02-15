# coding: utf-8
"""
Test script for Sps30 class testing that all class functionality is working.
"""
from sensors import sps30
import time

device_port = "/dev/ttyUSB0"
COUNT = 10
print('Device port set to:')
print(device_port)
print('******************')

sensor_sps30 = sps30.Sps30(device_port)

print('Sps30 __init__():')
print(sensor_sps30.ser.is_open)
print('----------')
print('Device information - product type:')
dipt = sensor_sps30.device_information()
print(dipt)


print('----------')
print('Testing close_port()')
sensor_sps30.close_port()
print('Port Status:')
print(sensor_sps30.ser.is_open)
print('Should be False\n')

print('----------')
print('Testing open_port()')
sensor_sps30.open_port()
print('Port Status:')
print(sensor_sps30.ser.is_open)
print('Should be True\n')


print('----------')
print('Device information - serial number:')
di2 = sensor_sps30.device_information(return_info='serial_number')
print(di2)
print('******************')


# FLOAT MODE
print('******************')
# Test start_measurement() default mode -> float values
# start_up_time recommended values depending on particle air values: 8,16 or 30 seconds.
print('----------')
print('Test start_measurement() default mode -> float values')
sensor_sps30.start_measurement(start_up_time=8)
print()

# Test read_measured_values() default mode -> float values
print('----------')
print('Test read_measured_values() default mode -> float values')
for i in range(COUNT):
    data_readout = sensor_sps30.read_measured_values()
    print('data output number' + str(i+1) + ':' + str(data_readout))
    print()
    time.sleep(1)
print()

# Test stop_measurement()
print('----------')
print('Test stop_measurement()')
sensor_sps30.stop_measurement()

# INTEGER MODE
print('******************')

# Test start_measurement() mode -> integer values
print('----------')
print('Test start_measurement() default mode -> integer values')
sensor_sps30.start_measurement(mode='integer', start_up_time=8)
print()

# Test read_measured_values() mode -> integer values
print('----------')
print('Test read_measured_values() default mode -> integer values')
for i in range(COUNT):
    data_readout = sensor_sps30.read_measured_values(mode='integer')
    print('data output number' + str(i+1) + ':' + str(data_readout))
    time.sleep(1)
print()

# Test stop_measurement()
print('----------')
print('Test stop_measurement()')
sensor_sps30.stop_measurement()

print('******************')
# Sleep -> Wake up -> Start fan cleaning
sleep = sensor_sps30.sleep()
print('sleep - ')
print(sleep)
print('sleeping 4 seconds...')
time.sleep(4)
wk = sensor_sps30.wake_up()
print('wake_up - ')
print(wk)


sensor_sps30.start_measurement()
sfc = sensor_sps30.start_fan_cleaning()
print('start_fan_clean - ' + str(sfc))
print('sleeping 7 seconds...')
time.sleep(7)
sensor_sps30.stop_measurement()

print('******************')
rd = sensor_sps30.read_version()
print('read_version -' + str(rd))
dr = sensor_sps30.device_reset()
print('device_reset - {dr}')

print('******************')
sensor_sps30.start_measurement(start_up_time=8)
rdsr = sensor_sps30.read_device_status_register()
print(rdsr)
print('sleeping 3 seconds...')
time.sleep(3)
sensor_sps30.stop_measurement()

sensor_sps30.close_port()
exit()
