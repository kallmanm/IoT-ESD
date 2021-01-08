"""
    Python class for control of the Sensirion SPS30 Particulate Matter Sensor.
    The Sps30 class below uses the UART Interface to control the sensor's functionality.
    See datasheet for detailed explanation of sensor:
    https://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/9.6_Particulate_Matter/Datasheets/Sensirion_PM_Sensors_SPS30_Datasheet.pdf
"""

import serial, struct, time



class Sps30:
    """
    Datasheet 5.0: UART Interface settings.
    """
    def __init__(self, port):
        self.port = port
        self.ser = serial.Serial(self.port,
                                 baudrate=115200,
                                 bytesize=serial.EIGHTBITS,
                                 stopbits=serial.STOPBITS_ONE,  # This is default class value
                                 parity=serial.PARITY_NONE,  # This is default class value
                                 timeout=2)  # Set at 2 seconds

    def byte_unstuffing(self, data):
        """
        Datasheet 5.2: Table 5 for details on byte-stuffing.
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
        Datasheet 5.2: Figure 4 MISO Frame.
        Return only RX data.
        """
        return data[5:-2]

    def start_measurement(self):
        """
        Datasheet 5.3.1
        """
        self.ser.write([0x7E, 0x00, 0x00, 0x02, 0x01, 0x03, 0xF9, 0x7E])
        time.sleep(30)  # Minimum time needed to boot up the sensor.

    def stop_measurement(self):
        """
        Datasheet 5.3.2
        """
        self.ser.write([0x7E, 0x00, 0x01, 0x00, 0xFE, 0x7E])

    def read_measured_values(self):
        """
        Datasheet 5.3.3
        """
        self.ser.flush.reset_input_buffer()  # Clear input buffer to ensure no leftover data in stream.
        self.ser.write([0x7E, 0x00, 0x03, 0x00, 0xFC, 0x7E])

        while True:
            data_to_read = self.ser.in_waiting()
            if data_to_read < 47:  # The MISO response frame for read_measured_values should be 47 long.
                break
            time.sleep(0.1)
        raw_data = self.ser.read(data_to_read)

        unstuffed_raw_data = self.byte_unstuffing(raw_data)  # Unstuffing the raw_data.
        byte_data = self.rx_data(unstuffed_raw_data)  # Fetching rx_data from byte_data.

        try:
            data = struct.unpack(">ffffffffff", byte_data)  # format = big-endian 10 floats
        except struct.error:
            data = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        return data

    def sleep(self):
        """
        Datasheet 5.3.4
        """
        pass

    def wake_up(self):
        """
        Datasheet 5.3.5
        """
        pass

    def start_fan_cleaning(self):
        """
        Datasheet 5.3.6
        """
        pass

    def read_write_auto_cleaning_interval(self):
        """
        Datasheet 5.3.7
        """
        pass

    def device_information(self):
        """
        Datasheet 5.3.8
        """
        pass

    def read_version(self):
        """
        Datasheet 5.3.9
        """
        pass

    def read_device_status_register(self):
        """
        Datasheet 5.3.10
        """
        pass

    def device_reset(self):
        """
        Datasheet 5.3.11
        """
        pass

