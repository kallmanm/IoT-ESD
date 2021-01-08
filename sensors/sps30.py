"""
    Python class for control of the Sensirion SPS30 Particulate Matter Sensor.
    The Sps30 class below uses the UART Interface to control the sensor's functionality.
    See datasheet for detailed explanation of sensor:
    https://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/9.6_Particulate_Matter/Datasheets/Sensirion_PM_Sensors_SPS30_Datasheet.pdf
"""

import serial, struct, time


#  TODO: Check configs for sensor
class Sps30:
    def __init__(self, port):
        self.port = port
        self.ser = serial.Serial(self.port,
                                 baudrate=115200,
                                 stopbits=serial.STOPBITS_ONE,  # This is default class value
                                 parity=serial.PARITY_NONE,  # This is default class value
                                 timeout=2)  # Set at 2 seconds

    def byte_unstuffing(self, data):
        """
            Datasheet 5.2 Table 5 for details on byte-stuffing.
        """
        print(f'Pre byte-unstuffing:{data}')
        if b'\x7D\x5E' in data:
            data = data.replace(b'\x7D\x5E', b'\x7E')
        if b'\x7D\x5D' in data:
            data = data.replace(b'\x7D\x5D', b'\x7D')
        if b'\x7D\x31' in data:
            data = data.replace(b'\x7D\x31', b'\x11')
        if b'\x7D\x33' in data:
            data = data.replace(b'\x7D\x33', b'\x13')
        print(f'Post byte-unstuffing:{data}')
        return data

    def rx_data(self, data):
        """
            Datasheet 5.2 Figure 4 MISO Frame.
            Return only RX data.
        """
        return data[5:-2]

    def start_measurement(self):
        self.ser.write([0x7E, 0x00, 0x00, 0x02, 0x01, 0x03, 0xF9, 0x7E])
        time.sleep(30)  # Minimum time needed to boot up the sensor.

    def stop_measurement(self):
        self.ser.write([0x7E, 0x00, 0x01, 0x00, 0xFE, 0x7E])

    def read_measured_values(self):
        self.ser.flush.reset_input_buffer()  # Clear input buffer to ensure no leftover data in stream.
        self.ser.write([0x7E, 0x00, 0x03, 0x00, 0xFC, 0x7E])

        data_to_read = self.ser.in_waiting()
        while data_to_read < 47:
            data_to_read = self.ser.in_waiting()
            time.sleep(0.1)
        raw_data = self.ser.read(data_to_read)

        raw_data = self.byte_unstuffing(raw_data)  # Unstuff the raw_data.
        byte_data = self.rx_data(raw_data)  # Fetch rx_data from  byte_data.

        try:
            data = struct.unpack(">ffffffffff", byte_data)  # format = big-endian 10 floats
        except struct.error:
            data = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        return data

