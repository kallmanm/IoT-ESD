"""
Utility functions.
"""
import yaml
import json
import base64


class CustomerTaskYaml:
    def __init__(self, params):
        self.params = params
        self.sensor = params.get('sensor')
        self.type = params.get('type')
        self.sample_amount = params.get('sample_amount')
        self.sample_rate = params.get('sample_rate')
        self.sample_size = params.get('sample_size')
        self.mode = params.get('mode')
        self.aggregate = params.get('aggregate')
        self.encrypt = params.get('encrypt')


def create_sensor_manager_yaml(input_yaml, save=False):
    # TODO: ADD SUPPORT FOR JSON
    with open(input_yaml) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    cty: CustomerTaskYaml = CustomerTaskYaml(**data)
    # TODO: modify data
    new_data = {
        'sensors': {f'{cty.sensor}': {'port': '/dev/ttyUSB0', 'debug': False}},
        'tasks': make_task(cty)
    }
    if save:
        with open(r'complex.yaml', 'w') as file:
            yaml.dump(new_data, file)

    return new_data


def make_task(obj):
    # start_measurement
    # read_measured_values
    tasks = [{f'{obj.sensor}': {'task': 'start_measurement',
                                'method_parameters': {'mode': f'{obj.mode}', 'start_up_time': 8}}},
             {f'{obj.sensor}': {'task': 'read_measured_values',
                                'measurement_samples': int(obj.samples),
                                'measurement_rate': int(obj.rate),
                                'measurement_amount': int(obj.amount),
                                'method_parameters': {'mode': f'{obj.mode}'}}}]
    # REMOVE IF STATEMENT IF NO OTHER TYPES THAN ALL ARE IMPLEMENTED
    if obj.type == 'all':
        # split data and return only what is requested
        pass
    if obj.aggregate:
        tasks.append({f'aggregate': obj.aggregate})
    if obj.encrypt:
        tasks.append({f'encrypt': obj.encrypt})
    # stop_measurement
    tasks.append({f'{obj.sensor}': {'task': 'stop_measurement'}})
    # close_port
    tasks.append({f'{obj.sensor}': {'task': 'close_port'}})

    return tasks


def encode_base64(data):
    # Encode data in base64
    to_string = json.dumps(data)
    to_bytes = str.encode(to_string)
    encoded = base64.b64encode(to_bytes)

    return encoded.decode()


def decode_base64(data):
    # Decode from base64
    to_bytes = base64.b64decode(data)

    return json.loads(to_bytes)
