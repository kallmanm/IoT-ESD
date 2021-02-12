"""
Utility functions.
"""
import yaml
import json
import base64


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
        self.type = params.get('type')
        self.samples = params.get('samples')
        self.rate = params.get('rate')
        self.amount = params.get('amount')
        self.mode = params.get('mode')
        self.aggregate = params.get('aggregate')
        self.encrypt = params.get('encrypt')


def create_sensor_manager_yaml(params, save=False):
    """
    Maps customer yaml file to sensor_manager yaml format.

    :param params: Customer data structure
    :param save: True if save to yaml file
    :return new_data: sensor_manager data structure.
    """
    cty: CustomerTaskYaml = CustomerTaskYaml(params)

    new_data = {
        'sensors': {f'{cty.sensor}': {'port': '/dev/ttyUSB0'}},
        'tasks': make_task(cty)
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
    """
    Encodes into base64.

    :param dict data:
    :return: encoded base64 string.
    """
    # Encode data in base64
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
    # Decode from base64
    to_bytes = base64.b64decode(data)

    return json.loads(to_bytes)
