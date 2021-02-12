"""
    A Python interface implementing the sps30 sensor library
"""
import time
import base64
import json
import numpy as np
from .sps30 import Sps30
# TODO: Add encrypt function


class SensorManager:
    # todo: fix
    """
    <COMMENT>

    :param type name: desc
    :return type name: desc

    """
    def __init__(self, sensors, tasks):
        # todo: fix
        """
        <COMMENT>

        :param type name: desc
        :return type name: desc

        """
        self.data = []
        for sensor in sensors:
            if 'sps30' in sensor:
                self.sps30 = Sps30(**sensors[sensor])
        self.sensors = sensors
        self.tasks = tasks
        self.data = {}
        self.log_data = []
        self.measurement_samples = 0
        self.measurement_rate = 0
        self.measurement_amount = 0
        self.encoded_data = ''
        self.data['device-name'] = self.get_device_name()
        self.data['serial-number'] = self.get_serial_number()
        # todo: add location to data.
        self.data['start-time'] = self.return_timestamp()
        self.data['stop-time'] = ''
        self.do_tasks()

    @staticmethod
    def return_timestamp():
        """
        Gets and returns the current local time.

        :return string timestamp: Current local time in format %Y-%m-%d %H:%M:%S %Z.
        """
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S %Z')
        return timestamp

    def sps30_task(self,
                   task,
                   measurement_samples=1,
                   measurement_rate=1,
                   measurement_amount=1,
                   method_parameters=None):
        # todo: fix desc
        # todo: ask john about naming convention for sample, rate and amount...
        """
        Performs the requested sps30 command.

        :param string task: the task to perform.
        :param measurement_samples:
        :param measurement_rate:
        :param method_parameters:
        :param measurement_amount:
        :return: The data from called method.

        """

        if task == 'start_measurement':
            return self.sps30.start_measurement(**method_parameters)

        elif task == 'read_measured_values':
            self.measurement_samples = measurement_samples
            self.measurement_rate = measurement_rate
            self.measurement_amount = measurement_amount
            sensor_data = {}
            for amount in range(measurement_amount):
                for sample in range(measurement_samples):
                    sensor_data[self.return_timestamp()] = self.sps30.read_measured_values(**method_parameters)
                    time.sleep(1)  # SPS30 needs 1 second between measurements.
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
        """
        Method that aggregates collected sensor data.

        Aggregates and divides upp data by self.measurement_amount attribute.

        :return dict aggregated_dic: data structured by key/value pairs.
        """

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
    def encrypt(data):
        # todo: fix desc
        """
        <COMMENT>

        :param type data: desc
        :return type name: desc
        """
        pass

    @staticmethod
    def encode_base64(data):
        # todo: fix desc
        """
        <COMMENT>

        :param type name: desc
        :return type name: desc
        """
        # Encode data in base64
        to_string = json.dumps(data)
        to_bytes = str.encode(to_string)
        encoded = base64.b64encode(to_bytes)

        return encoded.decode()

    @staticmethod
    def decode_base64(data):
        # todo: fix desc
        """
        <COMMENT>

        :param type name: desc
        :return type name: desc
        """
        # Decode from base64
        to_bytes = base64.b64decode(data)

        return json.loads(to_bytes)

    def do_tasks(self):
        # todo: fix desc
        """
        <COMMENT>

        :param type name: desc
        :return type name: desc
        """
        for index, task in enumerate(self.tasks):
            try:
                if 'sps30' in task.keys():
                    # check if read_measured_values
                    if task['sps30']['task'] == 'read_measured_values':
                        self.log_data.append('read_measured_values')
                        sensor_data = self.sps30_task(**task['sps30'])
                        self.data['sensor-data'] = sensor_data
                    elif task['sps30']['task'] == 'stop_measurement':
                        sensor_data = self.sps30_task(**task['sps30'])
                        self.log_data.append(sensor_data)
                        self.data['stop-time'] = self.return_timestamp()
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

    def get_device_name(self):
        """
        <COMMENT>

        :param type name: desc
        :return type name: desc
        """
        product_type = self.sps30.device_information(return_info='product_type')

        if product_type == '00080000\x00':
            return 'Sensirion SPS30 Particulate Matter Sensor'
        else:
            return 'Unknown Sensor Type'

    def get_serial_number(self):
        """
        <COMMENT>

        :return type name: desc
        """
        serial_number = self.sps30.device_information(return_info='serial_number')
        if serial_number.endswith('\x00'):
            serial_number = serial_number.replace('\x00', '')
        return serial_number
