from sensor_manager import SensorManager
from sm_utils import utils as u
import yaml
import argparse

# todo: fix script part to be able to use either customer format or admin format.
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
        # print(new_yaml)
        print('-------------')
        device = SensorManager(**new_yaml)
        # with admin yaml
        # device = SensorManagerMock(**yaml_instructions)
        print(device.encoded_data)
        print('-------------')
        print(device.decode_base64(device.encoded_data))
    except TypeError as e:
        print(f'Error: {e}')
    quit()
