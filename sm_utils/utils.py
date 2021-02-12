"""
Utility functions.
"""
import yaml
import json
import base64


def calculate_checksum(bytearray):
    # todo: add desc
    """add desc"""
    """
    The checksum is built before byte-stuffing and checked after removing stuffed bytes from the frame. The checksum
    is defined as follows:
    1. Sum all bytes between start and stop (without start and stop bytes).
    2. Take the least significant byte of the result and invert it. This will be the checksum.
    For a MOSI frame use Address, Command, Length and Data to calculate the checksum.
    For a MISO frame use Address, Command, State, Length and Data to calculate the checksum.
    """
    return 0xFF - sum(bytearray)


class CustomerTaskYaml:
    # todo: add desc
    """add desc"""
    def __init__(self, params):
        self.params = params
        self.sensor = params.get('sensor')
        self.type = params.get('type')
        self.samples = params.get('samples')
        self.rate = params.get('rate')
        self.amount = params.get('amount')
        self.mode = params.get('mode')
        self.aggregate = params.get('aggregate')
        self.encrypt = params.get('encrypt')


def create_sensor_manager_yaml(params, save=False):
    # TODO: ADD SUPPORT FOR JSON
    #with open(input_yaml) as f:
    #    data = yaml.load(f, Loader=yaml.FullLoader)
    cty: CustomerTaskYaml = CustomerTaskYaml(params)
    # TODO: modify data
    new_data = {
        'sensors': {f'{cty.sensor}': {'port': '/dev/ttyUSB0'}},
        'tasks': make_task(cty)
    }
    if save:
        with open(r'complex.yaml', 'w') as file:
            yaml.dump(new_data, file)

    return new_data


def make_task(obj):
    # todo: add desc
    """add desc"""
    tasks = [{f'{obj.sensor}': {'task': 'start_measurement',
                                'method_parameters': {'mode': f'{obj.mode}', 'start_up_time': 8}}},
             {f'{obj.sensor}': {'task': 'read_measured_values',
                                'measurement_samples': int(obj.samples),
                                'measurement_rate': int(obj.rate),
                                'measurement_amount': int(obj.amount),
                                'method_parameters': {'mode': f'{obj.mode}'}}},
             {f'{obj.sensor}': {'task': 'stop_measurement'}}]
    # todo: REMOVE IF STATEMENT IF NO OTHER TYPES THAN ALL ARE IMPLEMENTED
    if obj.type == 'all':
        # split data and return only what is requested
        pass
    if obj.aggregate:
        tasks.append({f'aggregate': obj.aggregate})
    if obj.encrypt:
        tasks.append({f'encrypt': obj.encrypt})
    # encode base64
    tasks.append({f'encode': True})
    # close_port
    tasks.append({f'{obj.sensor}': {'task': 'close_port'}})

    return tasks


def encode_base64(data):
    # todo: add desc
    """add desc"""
    # Encode data in base64
    to_string = json.dumps(data)
    to_bytes = str.encode(to_string)
    encoded = base64.b64encode(to_bytes)

    return encoded.decode()


def decode_base64(data):
    # todo: add desc
    """add desc"""
    # Decode from base64
    to_bytes = base64.b64decode(data)

    return json.loads(to_bytes)
