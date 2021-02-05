import yaml
import argparse
import time
import random
import base64
import json
import numpy as np
from sm_utils import utils as u


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
        for sensor in sensors:
            if 'sps30' in sensor:
                self.sps30 = Sps30Mock(**sensors[sensor])

        self.sensors = sensors
        self.tasks = tasks
        self.data = {}
        self.log_data = []
        self.measurement_samples = 0
        self.measurement_rate = 0
        self.measurement_amount = 0
        self.encoded_data = ''
        self.data['start-time'] = self.return_timestamp()
        self.do_tasks()
        self.data['stop-time'] = self.return_timestamp()

    @staticmethod
    def return_timestamp():
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S %Z')
        return timestamp

    def sps30_task(self,
                   task,
                   measurement_samples=1,
                   measurement_rate=1,
                   measurement_amount=1,
                   method_parameters=None):

        if task == 'start_measurement':
            return self.sps30.start_measurement(**method_parameters)

        elif task == 'read_measured_values':
            self.measurement_samples = measurement_samples
            self.measurement_rate = measurement_rate
            self.measurement_amount = measurement_amount
            sensor_data = {}
            for amount in range(measurement_amount):
                for sample in range(measurement_samples):
                    sensor_data[self.return_timestamp()] = self.sps30.read_measured_values(
                        **method_parameters)
                    time.sleep(1)
                if amount < measurement_amount - 1:
                    # TODO: change time.sleep to 60 when done with dev
                    # time.sleep(60 * measurement_rate - measurement_samples)
                    time.sleep(0.1)
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

    def aggregate(self):
        # aggregating keys
        keys = list(self.data['sensor-data'].keys())
        np_array_k = np.array(keys)
        split_array_k = np.array(np.array_split(np_array_k, self.measurement_amount))
        aggregated_keys = [k[-1].tolist() for k in split_array_k]

        # aggregating values
        values = list(self.data['sensor-data'].values())
        np_array_v = np.array(values)
        split_array_v = np.array(np.array_split(np_array_v, self.measurement_amount))
        aggregated_values = [v.mean(axis=0).tolist() for v in split_array_v]

        aggregated_dict = {key: value for (key, value) in zip(aggregated_keys, aggregated_values)}

        return aggregated_dict

    @staticmethod
    def encrypt(self, data):
        pass

    @staticmethod
    def encode_base64(data):
        # Encode data in base64
        to_string = json.dumps(data)
        to_bytes = str.encode(to_string)
        encoded = base64.b64encode(to_bytes)

        return encoded.decode()

    @staticmethod
    def decode_base64(data):
        # Decode from base64
        to_bytes = base64.b64decode(data)

        return json.loads(to_bytes)

    def do_tasks(self):
        for index, task in enumerate(self.tasks):
            try:
                if 'sps30' in task.keys():
                    # check if read_measured_values
                    if task['sps30']['task'] == 'read_measured_values':
                        self.log_data.append('read_measured_values')
                        result = self.sps30_task(**task['sps30'])
                        self.data['sensor-data'] = result
                    else:
                        result = self.sps30_task(**task['sps30'])
                        self.log_data.append(result)
                elif 'scd30' in task.keys():
                    msg = 'NOT IMPLEMENTED: scd30 task'
                    self.log_data.append(msg)
                elif 'svm30' in task.keys():
                    msg = 'NOT IMPLEMENTED: svm30 task'
                    self.log_data.append(msg)
                elif 'send_data' in task.keys():
                    # TODO: update SEND
                    msg = 'data sent!'
                    self.log_data.append(msg)
                elif 'aggregate' in task.keys():
                    self.data['sensor-data'] = self.aggregate()
                    self.log_data.append('data aggregated')
                elif 'encrypt' in task.keys():
                    # todo: update ENCRYPT
                    msg = 'data encrypted'
                    self.log_data.append(msg)
                elif 'encode' in task.keys():
                    encoded_data = self.encode_base64(self.data)
                    self.encoded_data += encoded_data
                else:
                    msg = f'Unsupported task attempted: {task}'
                    self.log_data.append(msg)
            except AttributeError as e:
                msg = f'Error in task:{task} - ErrorMessage:{e}'
                self.log_data.append(msg)


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
        # with customer yaml
        new_yaml = u.create_sensor_manager_yaml(**yaml_instructions)
        #print(new_yaml)
        print('-------------')
        device = SensorManagerMock(**new_yaml)
        # with admin yaml
        # device = SensorManagerMock(**yaml_instructions)
        #print(device.data)
        print(device.encoded_data)
        print('-------------')
        print(device.decode_base64(device.encoded_data))
    except TypeError as e:
        print(f'Error: {e}')
    quit()
