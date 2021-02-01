from sensors import sps30
import time
import argparse

# with open('sensors.yaml') as f:
#    data = yaml.load(f, Loader=yaml.FullLoader)
#    sensor_bridge_spec = data["sensor-bridge"]
#    svm30_spec = data["sensors"]["svm30"]
#    scd30_spec = data["sensors"]["scd30"]
#    print(svm30_spec)
#    print(scd30_spec)

# do actions if activated
# Maybe use Python IPC
# https://docs.python.org/3.7/library/ipc.html
# Asynchronous I/O shows promise... coroutines and tasks.


class SensorManager:
    def __init__(self, sensors, tasks):
        for sensor in sensors:
            if 'sps30' in sensor:
                self.sps30 = sps30.Sps30(**sensors[sensor])
        self.sensors = sensors
        self.tasks = tasks
        self.do_tasks()

    def sps30_task(self, task, measurement_samples=1, method_parameters=None):

        if task == 'start_measurement':
            self.sps30.start_measurement(**method_parameters)

        elif task == 'read_measured_values':
            sensor_data = []
            for sample in range(measurement_samples):
                stamp = time.strftime('%Y-%m-%d %H:%M:%S %Z')
                sensor_data.append(stamp)
                sensor_data.append(self.sps30.read_measured_values(**method_parameters))
                time.sleep(1)
            print(sensor_data)
            return sensor_data

        elif task == 'stop_measurement':
            self.sps30.stop_measurement()

        elif task == 'sleep':
            self.sps30.sleep()

        elif task == 'wake_up':
            self.sps30.wake_up()

        elif task == 'start_fan_cleaning':
            self.sps30.start_fan_cleaning()

        elif task == 'read_write_auto_cleaning_interval':
            self.sps30.read_write_auto_cleaning_interval()

        elif task == 'device_information':
            sensor_data = self.sps30.device_information(**method_parameters)
            return sensor_data

        elif task == 'read_version':
            self.sps30.read_version()

        elif task == 'read_device_status_register':
            self.sps30.read_device_status_register()

        elif task == 'device_reset':
            self.sps30.device_reset()

        elif task == 'open_port':
            self.sps30.open_port()

        elif task == 'close_port':
            self.sps30.close_port()

        else:
            sensor_data = f'invalid task: {task}'
            return sensor_data

    def do_tasks(self):
        for index, task in enumerate(self.tasks):
            if 'sps30' in task.keys():
                self.sps30_task(**task['sps30'])
            elif 'scd30' in task.keys():
                # TODO: scd30 method
                pass
            elif 'svm30' in task.keys():
                # TODO: svm30 method
                print('svm30 command')
                pass
            else:
                print(f'unsupported task attempted: {task}')



