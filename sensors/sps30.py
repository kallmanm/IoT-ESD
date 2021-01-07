import serial, struct, time


class Sps30:
    def __init__(self, port):
        self.port = port
        self.ser = serial.Serial(self.port, baudrate=115200, stopbits=1, parity="N", timeout=2)

    def start(self):
        # start command for sensor
        print('start')
        pass

    def stop(self):
        # stop command for sensor
        print('stop')
        pass

    def read(self):
        # reads data from sensor
        print('read')
        pass
