"""
Test script for Sps30 class testing that all class functionality is working.
"""
from ..sensors import sps30

device_port = "/dev/ttyUSB0"

# 1. Test __init__()
print(f'----------')
print(f'1. Test __init__()\n\n')
sensor_sps30 = sps30.Sps30(device_port, debug=True)
print(f'Sps30 activated: {sensor_sps30.ser.is_open}')
print(f'\n\n')

# 2. Test start_measurement() default mode -> float values
# start_up_time recommended values depending on particle air values: 8,16 or 30 seconds.
print(f'----------')
print(f'2. Test start_measurement() default mode -> float values')
sensor_sps30.start_measurement(start_up_time=16)
print(f'\n\n')

# 3. Test read_measured_values() default mode -> float values
# TODO: add test for integer mode
print(f'----------')
print(f'3. Test read_measured_values() default mode -> float values')
for i in range(5):
    data_readout = sensor_sps30.read_measured_values()
    print(f'data output number {i}: {data_readout}')
print(f'\n\n')

# 4. Test stop_measurement()
print(f'----------')
print(f'4. Test stop_measurement()')
sensor_sps30.stop_measurement()
print(f'\n\n')

# 5. Test close_port()
print(f'----------')
print(f'Test close_port()')
sensor_sps30.close_port()
print(f'Is port open: {sensor_sps30.ser.is_open}')
print(f'Should be False')
print(f'\n\n')

# 6. Test open_port()
print(f'----------')
print(f'6. Test open_port()')
sensor_sps30.open_port()
print(f'Is port open: {sensor_sps30.ser.is_open}')
print(f'Should be True')
print(f'\n\n')

# 7. Re-test read_measured_values() with reopened port
print(f'----------')
print(f'7. Re-test read_measured_values() with reopened port')
data_readout = sensor_sps30.read_measured_values()
print(f'data output: {data_readout}')
print(f'\n\n')

# TODO: add rest of tests
# 8. Test sleep()

# 9. Test wake_up()

# 10. Test start_fan_cleaning()

# 11. Test read_write_auto_cleaning_interval()

# 12. Test device_information() prod and serial info

# 13. Test read_version()

# 14. Test read_device_status_register()

# Ends test script
sensor_sps30.close_port()
exit()
