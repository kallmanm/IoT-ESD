from sensors import sps30
import time
import yaml
import argparse

# do actions if activated
# Maybe use Python IPC
# https://docs.python.org/3.7/library/ipc.html
# Asynchronous I/O shows promise... coroutines and tasks.


class SensorManager:
    def __init__(self, sensors, tasks):
        self.data = []
        for sensor in sensors:
            if 'sps30' in sensor:
                self.sps30 = sps30.Sps30(**sensors[sensor])
        self.sensors = sensors
        self.tasks = tasks
        self.do_tasks()

    def sps30_task(self, task, measurement_samples=1, method_parameters=None):

        if task == 'start_measurement':
            return self.sps30.start_measurement(**method_parameters)

        elif task == 'read_measured_values':
            sensor_data = []
            for sample in range(measurement_samples):
                stamp = time.strftime('%Y-%m-%d %H:%M:%S %Z')
                sensor_data.append(stamp)
                sensor_data.append(self.sps30.read_measured_values(**method_parameters))
                time.sleep(1)
            return sensor_data

        elif task == 'stop_measurement':
            return self.sps30.stop_measurement()

        elif task == 'sleep':
            return self.sps30.sleep()

        elif task == 'wake_up':
            return self.sps30.wake_up()

        elif task == 'start_fan_cleaning':
            return self.sps30.start_fan_cleaning()

        elif task == 'read_write_auto_cleaning_interval':
            return self.sps30.read_write_auto_cleaning_interval()

        elif task == 'device_information':
            sensor_data = self.sps30.device_information(**method_parameters)
            return sensor_data

        elif task == 'read_version':
            return self.sps30.read_version()

        elif task == 'read_device_status_register':
            return self.sps30.read_device_status_register()

        elif task == 'device_reset':
            return self.sps30.device_reset()

        elif task == 'open_port':
            return self.sps30.open_port()

        elif task == 'close_port':
            return self.sps30.close_port()

        else:
            sensor_data = f'invalid task: {task}'
            return sensor_data

    def do_tasks(self):
        for index, task in enumerate(self.tasks):
            try:
                if 'sps30' in task.keys():
                    result = self.sps30_task(**task['sps30'])
                    self.data.append(result)
                elif 'scd30' in task.keys():
                    msg = 'NOT IMPLEMENTED: scd30 task'
                    self.data.append(msg)
                elif 'svm30' in task.keys():
                    msg = 'NOT IMPLEMENTED: svm30 task'
                    self.data.append(msg)
                elif 'send_data' in task.keys():
                    # TODO: added data sending functionality
                    msg = 'data sent!'
                    self.data.append(msg)
                else:
                    msg = f'Unsupported task attempted: {task}'
                    self.data.append(msg)
                    print(msg)
            except AttributeError as err:
                msg = f'Error in task:{task} - ErrorMessage:{err}'
                self.data.append(msg)
                print(msg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c',
        dest='config_file',
        type=argparse.FileType(mode='r'))
    parser.add_argument(
        '--config-file',
        dest='config_file',
        type=argparse.FileType(mode='r'))
    args = parser.parse_args()
    yaml_instructions = yaml.load(args.config_file, Loader=yaml.FullLoader)
    try:
        sensor = SensorManager(**yaml_instructions)
    except TypeError as e:
        print(f'Error in yaml file.\nError: {e}')
    quit()
