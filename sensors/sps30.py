import serial, struct, time


#  TODO: Check configs for sensor
class Sps30:
    def __init__(self, port):
        self.port = port
        self.ser = serial.Serial(self.port,
                                 baudrate=115200,
                                 stopbits=serial.STOPBITS_ONE,  # This is default class value
                                 parity=serial.PARITY_NONE,  # This is default class value
                                 timeout=2)

    def start_sensor(self):
        self.ser.write([0x7E, 0x00, 0x00, 0x02, 0x01, 0x03, 0xF9, 0x7E])
        time.sleep(5)  # Minimum time needed to boot up the sensor.

    def stop_sensor(self):
        self.ser.write([0x7E, 0x00, 0x01, 0x00, 0xFE, 0x7E])

    def read_sensor_data(self):
        self.ser.flush.reset_input_buffer()
        self.ser.write([0x7E, 0x00, 0x03, 0x00, 0xFC, 0x7E])

        data_to_read = self.ser.in_waiting()
        while data_to_read < 47:
            data_to_read = self.ser.in_waiting()
            time.sleep(0.1)
        raw_data = self.ser.read(data_to_read)

        # Do byte-unstuffing
        # TODO:Code comes here...
        return raw_data

