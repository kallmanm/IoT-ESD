#!/usr/bin/python
import yaml
import argparse
import time
import random


class Sps30Mock:
    # 0
    def __init__(self, port, debug=False):
        self.port = port
        self.ser = {'port': self.port, 'baudrate': 115200, 'bytesize': 8, 'stopbits': 1, 'parity': None, 'timeout': 2}
        self.debug = debug
        print('Sps30_mock.__init__()')
        print(f'{self.ser}')

    def mock_float(self):
        mf = round(random.uniform(0.00, 2.00), 2)
        return mf

    def mock_int(self):
        mi = random.randint(0, 9)
        return mi

    # 1
    def start_measurement(self, mode='float', start_up_time=30):
        res = 'start_measurement activated'
        return res

    # 2
    def stop_measurement(self):
        res = 'stop_measurement activated'
        return res

    # 3
    def read_measured_values(self, mode='float'):
        # print(f'measuring with mode: {mode}')
        if mode == 'integer':
            data = (self.mock_int(), self.mock_int(), self.mock_int(), self.mock_int(),
                    self.mock_int(), self.mock_int(), self.mock_int(), self.mock_int(),
                    self.mock_int(), self.mock_int())
        else:
            data = (self.mock_float(), self.mock_float(), self.mock_float(),
                    self.mock_float(), self.mock_float(), self.mock_float(),
                    self.mock_float(), self.mock_float(), self.mock_float(),
                    self.mock_float())

        return data

    # 4
    def sleep(self):
        res = 'sleep mode activated'
        return res

    # 5
    def wake_up(self):
        res = 'wake_up activated'
        return res

    # 6
    def start_fan_cleaning(self):
        res = 'start_fan_cleaning activated'
        return res

    # 7
    def read_write_auto_cleaning_interval(self):
        res = 'read_write_auto_cleaning_interval activated'
        return res

    # 8
    def device_information(self, return_info='product_type'):
        res = f'device_information activated: {return_info}'
        return res

    # 9
    def read_version(self):
        res = f'read_version activated: 0008000'
        return res

    # 10
    def read_device_status_register(self):
        res = f'read_device_status_register activated'
        return res

    # 11
    def device_reset(self):
        res = f'device_reset activated'
        return res

    # 12
    def open_port(self):
        res = f'port_open activated'
        return res

    # 13
    def close_port(self):
        res = f'close_port activated'
        return res


class SensorManagerMock:
    def __init__(self, sensors, tasks):
        for SENSOR in sensors:
            if 'sps30' in SENSOR:
                self.sps30 = Sps30Mock(**sensors[SENSOR])

        self.sensors = sensors
        self.tasks = tasks
        self.data = []
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
                    msg = 'data sent!'
                    self.data.append(msg)
                else:
                    msg = f'Unsupported task attempted: {task}'
                    self.data.append(msg)
            except AttributeError as e:
                msg = f'Error in task:{task} - ErrorMessage:{e}'
                self.data.append(msg)


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
        sensor = SensorManagerMock(**yaml_instructions)
    except TypeError as e:
        print(f'Error in yaml file.\nError: {e}')
    quit()
