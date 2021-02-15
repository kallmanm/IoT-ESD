"""
Utility functions.
"""
import yaml
import json
import base64
import time

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from cryptography.fernet import Fernet


class CustomerTaskYaml:
    """
    Maps customer yaml to CustomerTaskYaml object.
    """

    def __init__(self, params):
        """
        Constructor for CustomerTaskYaml.

        :param params: data structure.
        """
        self.params = params
        self.sensor = params.get('sensor')
        self.mode = params.get('mode')
        self.type = params.get('type')
        self.samples = params.get('samples')
        self.rate = params.get('rate')
        self.amount = params.get('amount')
        self.aggregate = params.get('aggregate')
        self.encrypt = params.get('encrypt')
        if self.encrypt:
            self.pub_key = params.get('pub_key')


def create_sensor_manager_yaml(params, save=False):
    """
    Maps customer yaml file to sensor_manager yaml format.

    :param params: Customer data structure
    :param save: True if save to yaml file
    :return new_data: sensor_manager data structure.
    """
    cty = CustomerTaskYaml(params)

    new_data = {
        'sensors': {{cty.sensor}: {'port': '/dev/ttyUSB0'}},
        'tasks': make_task(cty),
        'pub_key': cty.pub_key
    }
    if save:
        with open(r'complex.yaml', 'w') as file:
            yaml.dump(new_data, file)

    return new_data


def make_task(obj):
    """

    :param obj: CustomerTaskYaml object as input.
    :return tasks: Returns tasks in correct format for sensor_manager.
    """
    tasks = [{{obj.sensor}: {'task': 'start_measurement',
                             'method_parameters': {'mode': {obj.mode}, 'start_up_time': 8}}},
             {{obj.sensor}: {'task': 'read_measured_values',
                             'measurement_samples': int(obj.samples),
                             'measurement_rate': int(obj.rate),
                             'measurement_amount': int(obj.amount),
                             'method_parameters': {'mode': {obj.mode}}}},
             {{obj.sensor}: {'task': 'stop_measurement'}}]
    # todo: REMOVE IF STATEMENT IF NO OTHER TYPES THAN ALL ARE IMPLEMENTED
    if obj.type == 'all':
        # split data and return only what is requested
        pass
    if obj.aggregate:
        tasks.append({'aggregate': obj.aggregate})
    if obj.encrypt:
        tasks.append({'encrypt': obj.encrypt})
    # encode base64
    tasks.append({'encode': True})
    # close_port
    tasks.append({'{obj.sensor}': {'task': 'close_port'}})

    return tasks


def encode_base64(data):
    """
    Encodes into base64.

    :param dict data:
    :return: encoded base64 string.
    """
    to_string = json.dumps(data)
    to_bytes = str.encode(to_string)
    encoded = base64.b64encode(to_bytes)

    return encoded.decode()


def decode_base64(data):
    """
    decodes from base64.

    :param  string data:
    :return: dict object.
    """
    to_bytes = base64.b64decode(data)

    return json.loads(to_bytes)


def return_timestamp():
    """
    Gets and returns the current local time.

    :return string timestamp: Current local time in format %Y-%m-%d %H:%M:%S %Z.
    """
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S %Z')

    return timestamp


#####################################
#   ENCRYPTION/DECRYPTION SECTION   #
#####################################


class Encryptor:
    """
    Encryptor Class desc.
    """

    def __init__(self, data_to_encrypt, asym_pub_key):
        """
        Constructor.
        """
        self.data_to_encrypt = data_to_encrypt
        self.asym_pub_key = asym_pub_key

        self.sym_key = self.generate_sym_key()
        self.fernet = Fernet(self.sym_key)

        # data to send customer, encrypted with self.sym_key
        self.encrypted_data = self.symmetrical_encryption()
        # key to send customer, encrypted with self.asym_pub_key
        self.encrypted_sym_key = self.asymmetrical_encryption()

    def generate_sym_key(self):
        """
        Generates a symmetrical key and returns it.
        """
        _sym_key = Fernet.generate_key()
        return _sym_key

    def symmetrical_encryption(self):
        """
        Desc
        """
        sym_encrypted_data = self.fernet.encrypt(self.data_to_encrypt)

        return sym_encrypted_data

    def asymmetrical_encryption(self):
        """
        Desc
        """
        # public_key = serialization.load_pem_public_key(self.asym_pub_key, backend=default_backend())

        encrypted_key = self.asym_pub_key.encrypt(
            self.sym_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            ))

        return encrypted_key

    def return_key_and_data(self):
        key = self.encrypted_sym_key
        data = self.encrypted_data

        return key, data


class Decryptor:
    """
    Decryptor Class desc.
    """

    def __init__(self, data_to_decrypt, encrypted_sym_key, asym_private_key):
        """
        Constructor.
        """
        self.data_to_decrypt = data_to_decrypt
        self.encrypted_sym_key = encrypted_sym_key
        self.asym_private_key = asym_private_key

        self.decrypted_sym_key = self.asymmetrical_decryption()
        self.fernet = Fernet(self.decrypted_sym_key)
        self.decrypted_data = self.symmetrical_decryption()

    def asymmetrical_decryption(self):
        decrypted_data = self.asym_private_key.decrypt(
            self.encrypted_sym_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            ))

        return decrypted_data

    def symmetrical_decryption(self):
        """
        Decrypts an encrypted message
        """
        return self.fernet.decrypt(self.data_to_decrypt)

    def return_key_and_data(self):
        key = self.decrypted_sym_key
        data = self.decrypted_data

        return key, data


def encode_base64_key_and_data(key, data):
    """
    Desc
    """
    # CONVERT key AND data FROM BYTES -> STRING
    key_bytes_to_string = key.decode('latin1')
    data_bytes_to_string = data.decode()

    # CREATE DICT OBJECT
    data_to_dict = {
        'key': key_bytes_to_string,
        'data': data_bytes_to_string
    }

    # ENCODE data_to_dict INTO BASE64
    encoded_data = encode_base64(data_to_dict)

    return encoded_data


def decode_base64_key_and_data(base64_string):
    """
    Desc
    """
    data = decode_base64(base64_string)

    key_to_bytes = data['key'].encode('latin1')
    data_to_bytes = data['data'].encode()

    return key_to_bytes, data_to_bytes
