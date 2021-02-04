"""
Utility functions.
"""
import yaml


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
    with open(input_yaml) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    obj = CustomerTaskYaml(**data)
    # TODO: modify data
    new_data = {
        'sensors': {f'{obj.sensor}': {'port': '/dev/ttyUSB0', 'debug': False}},
        'tasks': make_task(obj)
    }
    if save:
        with open(r'complex.yaml', 'w') as file:
            documents = yaml.dump(new_data, file)
    return new_data


def make_task(obj):
    # start_measurement
    # read_measured_values
    tasks = [{f'{obj.sensor}': {'task':
                                'start_measurement',
                                'method_parameters': {
                                    'mode': f'{obj.mode}',
                                    'start_up_time': 8}}},
             {f'{obj.sensor}': {'task':
                                'read_measured_values',
                                'measurement_samples': int(obj.sample_amount),
                                'method_parameters': {'mode': f'{obj.mode}'}}
              }]

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
