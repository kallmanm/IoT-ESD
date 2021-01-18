"""
    A python class for control of the Sensirion SPS30 Particulate Matter Sensor.
    The Sps30 class below uses the UART Interface to control the sensor's functionality.

    Datasheet: <add link to datasheet>

    All 'Datasheet x.x' references in methods refers to the specific sections in above referenced datasheet.
"""

import serial
import struct
import time


class Sps30:
    """
    Initializing to default sps30 settings.
    Datasheet 5.0: UART Interface settings.
    """

    def __init__(self, port, debug=False):
        self.port = port
        self.ser = serial.Serial(self.port,
                                 baudrate=115200,
                                 bytesize=serial.EIGHTBITS,
                                 stopbits=serial.STOPBITS_ONE,  # This is default class value
                                 parity=serial.PARITY_NONE,  # This is default class value
                                 timeout=2)  # Set at 2 seconds
        self.debug = debug

    def byte_unstuffing(self, data):
        """
        Datasheet 5.2: Table 5 for details on byte-stuffing.
        """

        if self.debug:
            print(f'Pre byte_unstuffing:{data}')
        if b'\x7D\x5E' in data:
            data = data.replace(b'\x7D\x5E', b'\x7E')
        if b'\x7D\x5D' in data:
            data = data.replace(b'\x7D\x5D', b'\x7D')
        if b'\x7D\x31' in data:
            data = data.replace(b'\x7D\x31', b'\x11')
        if b'\x7D\x33' in data:
            data = data.replace(b'\x7D\x33', b'\x13')
        if self.debug:
            print(f'Post byte_unstuffing:{data}')

        return data

    @staticmethod
    def error_msg_check(byte):
        """
        Datasheet 5.2: Table 6 Error Codes.
        :param byte: byte
        :return error_msg:
        """

        error_msg = ""

        if byte == b'\x00':
            error_msg = 'No error'
        if byte == b'\x01':
            error_msg = 'Wrong data length for this command (too much or little data)'
        if byte == b'\x02':
            error_msg = 'Unknown command'
        if byte == b'\x03':
            error_msg = 'No access right for command'
        if byte == b'\x04':
            error_msg = 'Illegal command parameter or parameter out of allowed range'
        if byte == b'\x28':
            error_msg = 'Internal function argument out of range'
        if byte == b'\x43':
            error_msg = 'Command not allowed in current state'

        return error_msg

    def start_measurement(self, mode='float', start_up_time=30):
        """
        Datasheet 5.3.1
        Measurement Output Format:
        0x03: Big-endian IEEE754 float values
        0x05: Big-endian unsigned 16-bit integer values
        Function default set to Big-endian IEEE754 float values.
        """

        # mode = float cmd
        cmd = [0x7E, 0x00, 0x00, 0x02, 0x01, 0x03, 0xF9, 0x7E]

        if mode == 'integer':
            cmd = [0x7E, 0x00, 0x00, 0x02, 0x01, 0x05, 0xF7, 0x7E]

        self.ser.write(cmd)

        if self.debug:
            raw_response = self.ser.read(7)
            response = self.byte_unstuffing(raw_response)
            error_msg = self.error_msg_check(response[3])
            print(f'Response Status start_measurement(): {error_msg}')

        time.sleep(start_up_time)  # Minimum time needed to boot up the sensor.

    def stop_measurement(self):
        """
        Datasheet 5.3.2
        """

        self.ser.write([0x7E, 0x00, 0x01, 0x00, 0xFE, 0x7E])

        if self.debug:
            raw_response = self.ser.read(7)
            response = self.byte_unstuffing(raw_response)
            error_msg = self.error_msg_check(response[3])
            print(f'Response Status stop_measurement(): {error_msg}')

    def read_measured_values(self, mode='float'):
        """
        Datasheet 5.3.3
        """

        if mode == 'integer':
            stop_value = 27
        else:
            stop_value = 47

        self.ser.reset_input_buffer()  # Clear input buffer to ensure no leftover data in stream.
        self.ser.write([0x7E, 0x00, 0x03, 0x00, 0xFC, 0x7E])

        while True:
            data_to_read = self.ser.in_waiting()
            print(f'data_to_read value at: {data_to_read}')
            if data_to_read >= stop_value:  # The MISO response frame for read_measured_values should be 27 or 47 long.
                break
            time.sleep(0.1)
        raw_data = self.ser.read(data_to_read)

        unstuffed_raw_data = self.byte_unstuffing(raw_data)  # Unstuffing the raw_data.

        if self.debug:
            error_flag = unstuffed_raw_data[3]
            error_msg = self.error_msg_check(error_flag)
            print(f'Response Status read_measured_values(): {error_msg}')

        # Datasheet 5.2: Figure 4 MISO Frame.
        rx_data = unstuffed_raw_data[5:-2]  # Removing header and tail bits.

        if mode == 'integer':
            try:
                data = struct.unpack(">iiiiiiiiii", rx_data)  # format = big-endian 10 integers
            # TODO: improve error handling
            except struct.error:
                data = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        else:
            try:
                data = struct.unpack(">ffffffffff", rx_data)  # format = big-endian 10 floats
            # TODO: improve error handling
            except struct.error:
                data = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

        return data

    def sleep(self):
        """
        Datasheet 5.3.4
        """

        self.ser.reset_input_buffer()
        self.ser.write([0x7E, 0x00, 0x10, 0x00, 0xEF, 0x7E])

        if self.debug:
            raw_response = self.ser.read(7)
            response = self.byte_unstuffing(raw_response)
            error_msg = self.error_msg_check(response[3])
            print(f'Response Status sleep(): {error_msg}')

    def wake_up(self):
        """
        Datasheet 5.3.5
        """

        self.ser.reset_input_buffer()
        self.ser.write([0xFF])
        self.ser.write([0x7E, 0x00, 0x11, 0x00, 0xEE, 0x7E])

        if self.debug:
            raw_response = self.ser.read(7)
            response = self.byte_unstuffing(raw_response)
            error_msg = self.error_msg_check(response[3])
            print(f'Response Status wake_up(): {error_msg}')

    def start_fan_cleaning(self):
        """
        Datasheet 5.3.6
        """

        self.ser.reset_input_buffer()
        self.ser.write([0x7E, 0x00, 0x56, 0x00, 0xA9, 0x7E])

        if self.debug:
            raw_response = self.ser.read(7)
            response = self.byte_unstuffing(raw_response)
            error_msg = self.error_msg_check(response[3])
            print(f'Response Status start_fan_cleaning(): {error_msg}')

    def read_write_auto_cleaning_interval(self):
        """
        Datasheet 5.3.7
        """

        # TODO: Review code and method
        self.ser.reset_input_buffer()
        # Read Auto Cleaning Interval:
        self.ser.write([0x7E, 0x00, 0x80, 0x01, 0x00, 0x7D, 0x5E, 0x7E])
        # Write Auto Cleaning Interval to 0 (disable):
        # Disabled, use with caution.
        # self.ser.write([0x7E, 0x00, 0x80, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7A, 0x7E])

    def device_information(self, return_info='product_type'):
        """
        Datasheet 5.3.8
        response info:
            Requested Device Information as null-terminated ASCII string.
            The size of the string is limited to 32 ASCII characters (including null character).
        """

        # default set to product_type
        cmd = 0x00
        check = 0x2E
        stop_value = 16

        if return_info == 'serial_number':
            cmd = 0x03
            check = 0x2B
            stop_value = 28

        self.ser.reset_input_buffer()
        self.ser.write([0x7E, 0x00, 0xD0, 0x01, cmd, check, 0x7E])

        while True:
            data_to_read = self.ser.in_waiting()
            if data_to_read >= stop_value:
                break
            time.sleep(0.1)
        raw_data = self.ser.read(data_to_read)

        unstuffed_raw_data = self.byte_unstuffing(raw_data)  # Unstuffing the raw_data.

        if self.debug:
            error_flag = unstuffed_raw_data[3]
            error_msg = self.error_msg_check(error_flag)
            print(f'Response Status device_information(): {error_msg}')

        rx_data = unstuffed_raw_data[5:-2]  # Removing header and tail bits.

        data = rx_data.decode('ascii')

        return data

    def read_version(self):
        """
        Datasheet 5.3.9
        """

        stop_value = 14
        self.ser.reset_input_buffer()
        self.ser.write([0x7E, 0x00, 0xD1, 0x00, 0x2E, 0x7E])

        while True:
            data_to_read = self.ser.in_waiting()
            if data_to_read >= stop_value:
                break
            time.sleep(0.1)
        raw_data = self.ser.read(data_to_read)

        unstuffed_raw_data = self.byte_unstuffing(raw_data)  # Unstuffing the raw_data.

        if self.debug:
            error_flag = unstuffed_raw_data[3]
            error_msg = self.error_msg_check(error_flag)
            print(f'Response Status device_information(): {error_msg}')

        rx_data = unstuffed_raw_data[5:-2]  # Removing header and tail bits.

        try:
            data = struct.unpack(">bbbbbbb", rx_data)  # format = big-endian 7  uint8 integers
        except struct.error:
            data = "error in read_version fetch."

        return data

    def read_device_status_register(self):
        """
        Datasheet 5.3.10
        """

        self.ser.reset_input_buffer()
        self.ser.write([0x7E, 0x00, 0xD2, 0x01, 0x00, 0x2C, 0x7E])
        # TODO: add self.ser.read() functionality to read response.
        # TODO: add self.debug check to confirm error status flag

    def device_reset(self):
        """
        Datasheet 5.3.11
        """

        self.ser.reset_input_buffer()
        self.ser.write([0x7E, 0x00, 0xD3, 0x00, 0x2C, 0x7E])

        if self.debug:
            raw_response = self.ser.read(7)
            response = self.byte_unstuffing(raw_response)
            error_msg = self.error_msg_check(response[3])
            print(f'Response Status device_reset(): {error_msg}')

    def open_port(self):
        """
        Opens a port connection.
        """

        self.ser = serial.Serial(self.port,
                                 baudrate=115200,
                                 bytesize=serial.EIGHTBITS,
                                 stopbits=serial.STOPBITS_ONE,  # This is default class value
                                 parity=serial.PARITY_NONE,  # This is default class value
                                 timeout=2)  # Set at 2 seconds

    def close_port(self):
        """
        Closes the port connection immediately.
        """

        self.ser.close()
