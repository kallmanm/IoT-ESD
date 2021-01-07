import serial, struct, time


class Sps30:
    def __init__(self, port):
        self.port = port
        self.serial = serial.Serial(self.port, baudrate=115200, stopbits=1, parity="N", timeout=2)

    def start(self):
        # start command for sensor
        pass

    def stop(self):
        # stop command for sensor
        pass

    def read(self):
        # reads data from sensor
        pass
