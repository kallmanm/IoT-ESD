# todo: fix licence
"""
    A Python interface implementing the sps30 sensor library.

    The interface allows you to control and issue commands to the selected sensor via a json object.
    See sensor_manager_cli.py for example implementation.

    by
    Mattias Kallman
    Github: @kallmanm
    LinkedIn: www.linkedin.com/in/mattias-kallman

    <insert copyright notice>

    <insert LICENSE>

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""
import time
import base64
import json
import numpy as np
import sensors.sps30 as sps30
from sm_utils.utils import Encryptor, encode_base64_key_and_data, encode_base64, return_timestamp


class SensorManager:
    """
    SensorManager Class controls and performs the sensor operations according to given json instructions.

    When The SensorManager Class is instantiated it takes in as kwargs 'sensors' and 'tasks'. As the
    constructor is instantiating it reads in the sensor information and opens a connection to given
    sensors. After that all key attributes are instantiated and finally the do_tasks() method is run
    that performs the sensor operations.
    """
    def __init__(self, sensors, tasks, pub_key=None):
        """
        Constructor for SensorManager Class.

        :param sensors: Sensors information.
        :param tasks:  Tasks to perform with Sensors.
        """
        self.data = []
        for sensor in sensors:
            if 'sps30' in sensor:
                self.sps30 = sps30.Sps30(**sensors[sensor])
        self.sensors = sensors
        self.tasks = tasks
        self.data = {}
        self.log_data = []
        self.measurement_samples = 0
        self.measurement_rate = 0
        self.measurement_amount = 0
        # todo: make sure pub_key is read in correctly
        self.pub_key = pub_key
        self.encrypted_data = ''
        self.encoded_data = ''
        self.data['device-name'] = self.get_device_name()
        self.data['serial-number'] = self.get_serial_number()
        self.data['start-time'] = return_timestamp()
        self.data['stop-time'] = ''
        self.do_tasks()

    def sps30_task(self,
                   task,
                   measurement_samples=1,
                   measurement_rate=1,
                   measurement_amount=1,
                   method_parameters=None):
        """
        Performs the requested sps30 command.

        :param string task: the task to perform.
        :param measurement_samples: The amount of samples to take per measurement_amount.
        :param measurement_rate: The rate at which to space the measurements. 1-5 min.
        :param method_parameters: Dict object containing necessary parameters to perform tasks.
        :param measurement_amount: Total amount of measurements to be done.
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
                    sensor_data[return_timestamp()] = self.sps30.read_measured_values(**method_parameters)
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
            sensor_data = {'invalid task': task}
            return sensor_data

    def aggregate(self):
        """
        Method that aggregates collected sensor data.

        Aggregates and divides upp data by self.measurement_amount attribute.

        :return dict aggregated_dic: data structured by key/value pairs.
        """

        # Aggregating keys
        keys = list(self.data['sensor-data'].keys())
        np_array_k = np.array(keys)
        split_array_k = np.array(np.array_split(np_array_k, self.measurement_amount))
        aggregated_keys = [k[-1].tolist() for k in split_array_k]

        # Aggregating values
        values = list(self.data['sensor-data'].values())
        np_array_v = np.array(values)
        split_array_v = np.array(np.array_split(np_array_v, self.measurement_amount))
        aggregated_values = [v.mean(axis=0).tolist() for v in split_array_v]

        # Structure into dict
        aggregated_dict = {key: value for (key, value) in zip(aggregated_keys, aggregated_values)}

        return aggregated_dict

    def encrypt(self):
        """
        Method that encrypts data.

        :param data: Data to encrypt.
        :param public_key: Public key used to encrypt data.
        :return encrypted_data: Data that has been encrypted.
        """
        # PUBLIC KEY TO ENCRYPT

        #  PYTHON LIB FOR ENCRYPTION
        #  https://cryptography.io/en/latest/

        #  GENERAL INFO ON ENCRYPTION
        #  https://en.wikipedia.org/wiki/Public-key_cryptography

        #  SYMMETRIC EXAMPLE
        #  https://devqa.io/encrypt-decrypt-data-python/

        #  ASYMMETRIC EXAMPLE
        #  https://towardsdatascience.com/asymmetric-encrypting-of-sensitive-data-in-memory-python-e20fdebc521c

        encrypted_data = self.data
        # todo: 1. Data MUST be converted to bytes before fed into ENCRYPTOR CLASS
        # todo: 2. Use Ecryptor class to make encrypted data
        # todo: 3. Use encode_base64_key_and_data()

        return encrypted_data

    def do_tasks(self):
        """
        Method that performs the given tasks for the sensors.

        Saves the tasks results in self.data and self.log_data.
        """
        # If a new task is created it needs to also be added in the try/except within the for loop,
        # otherwise do_tasks() won't be able to interpret the command.
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
                        self.data['stop-time'] = return_timestamp()
                    else:
                        result = self.sps30_task(**task['sps30'])
                        self.log_data.append(result)
                elif 'scd30' in task.keys():
                    msg = 'NOT IMPLEMENTED: scd30 task'
                    self.log_data.append(msg)
                elif 'svm30' in task.keys():
                    msg = 'NOT IMPLEMENTED: svm30 task'
                    self.log_data.append(msg)
                # TODO: CHECK THAT AGGREGATE; ENCRYPT AND ENCODE WORK WITH NEW SETUP
                elif 'aggregate' in task.keys():
                    print(f"task['aggregate']:{task['aggregate']}")
                    if task['aggregate']:
                        self.data['sensor-data'] = self.aggregate()
                        self.log_data.append('data aggregated')
                elif 'encrypt' in task.keys():
                    print(f"task['encrypt']:{task['encrypt']}")
                    if task['encrypt']:
                        self.encrypted_data = self.encrypt()
                        msg = 'data encrypted'
                        self.log_data.append(msg)
                elif 'encode' in task.keys():
                    print(f"task['encode']:{task['encode']}")
                    if task['encode']:
                        if task['encrypt']:
                            encoded_data = encode_base64_key_and_data(self.pub_key, self.data)
                            self.encoded_data = encoded_data
                        else:
                            encoded_data = encode_base64(self.data)
                            self.encoded_data = encoded_data
                else:
                    msg = {'Unsupported task attempted': task}
                    self.log_data.append(msg)
            except AttributeError as e:
                msg = {'Error': e}
                self.log_data.append(msg)

    def get_device_name(self):
        """
        Fetches the sensors device name.

        Currently only configured to fetch data from sps30 sensor.

        :return type name: the device name.
        """
        product_type = self.sps30.device_information(return_info='product_type')

        if product_type == '00080000\x00':
            return 'Sensirion SPS30 Particulate Matter Sensor'
        else:
            return 'Unknown Sensor Type'

    def get_serial_number(self):
        """
        Fetches the sensors device serial number.

        Currently only configured to fetch data from sps30 sensor.

        :return string serial_number: the device serial number.
        """
        serial_number = self.sps30.device_information(return_info='serial_number')
        if serial_number.endswith('\x00'):
            serial_number = serial_number.replace('\x00', '')
        return serial_number

    def save_to_json(self):
        # TODO: implement
        pass

    def save_to_json(self):
        # TODO: implement
        pass
