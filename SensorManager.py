# IMPORT Sensirion modules for sensor management


class Sensor:
    power = 'off'

    def __init__(self, config):
        self.config

    def check_sensor_status(self):
        return True

    def power_on(self):
        power = 'on'
        print(f'The power is {power}')
        # run functionality to turn on sensor if needed.

    def power_off(self):
        power = 'off'
        print(f'The power is {power}')
        # run functionality to turn off sensor if needed.

    def collect_data(self):
        try:
            if self.check_sensor_status():
                pass

        except RuntimeError as e:
            print(f'{e}')

