"""
    A python class for control of the Sensirion SPS30 Particulate Matter Sensor.
    The Sps30 class below uses the UART Interface to control the sensor's functionality.

    Datasheet: <add link to datasheet>

    All 'Datasheet x.x' references in methods refers to the specific sections in above referenced datasheet.
"""

import serial
import struct
import time


# TODO: 1. add returns on all sensor methods
# TODO: 2. fix byte stuff/unstuff
# https://sensirion.github.io/python-shdlc-driver/_modules/sensirion_shdlc_driver/serial_frame_builder.html


class Sps30:
    """
    Initializing to default sps30 settings.
    Datasheet 5.0: UART Interface settings.
    """

    START_STOP_BYTE = 0x7E
    ESCAPE_BYTE = 0x7D
    ESCAPE_XOR = 0x20
    CHARS_TO_ESCAPE = [START_STOP_BYTE, ESCAPE_BYTE, 0x11, 0x13]

    def __init__(self, port, debug=False):
        self.port = port
        self.ser = serial.Serial(self.port,
                                 baudrate=115200,
                                 bytesize=serial.EIGHTBITS,
                                 stopbits=serial.STOPBITS_ONE,  # This is default class value
                                 parity=serial.PARITY_NONE,  # This is default class value
                                 timeout=2)  # Set at 2 seconds
        self.debug = debug

    @staticmethod
    def calculate_checksum(list_of_bytes):
        """
        The checksum is built before byte-stuffing and checked after removing stuffed bytes from the frame.
        The checksum is defined as follows:
        1. Sum all bytes between start and stop (without start and stop bytes).
        2. Take the least significant byte of the result and invert it. This will be the checksum.
        For a MOSI frame use Address, Command, Length and Data to calculate the checksum.
        For a MISO frame use Address, Command, State, Length and Data to calculate the checksum.
        :param bytearray list_of_bytes:
        :return checksum byte:
        """
        return 0xFF - sum(list_of_bytes)

    @staticmethod
    def byte_stuffing(frame):
        """
        Datasheet 5.2: Table 5 for details on byte-stuffing.
        """
        """
            REWRITE IN OWN WORDS. USE THIS FORMAT
                Perform byte-stuffing (escape reserved bytes).

                :param bytearray data: The data without stuffed bytes.
                :return: The data with stuffed bytes.
                :rtype: bytearray
        """
        new_frame = bytearray()

        if b'\x7E' in frame:
            frame = frame.replace(b'\x7E', b'\x7D\x5E')
        if b'\x7D' in frame:
            frame = frame.replace(b'\x7D', b'\x7D\x5D')
        if b'\x11' in frame:
            frame = frame.replace(b'\x11', b'\x7D\x31')
        if b'\x13' in frame:
            frame = frame.replace(b'\x13', b'\x7D\x33')

        return frame

    @staticmethod
    def undo_byte_stuffing(frame):
        """
        Datasheet 5.2: Table 5 for details on byte-unstuffing.
        """
        """
        REWRITE IN OWN WORDS. USE THIS FORMAT
                Undo byte-stuffing (replacing stuffed bytes by their original value).

                :param bytearray stuffed_data: The data with stuffed bytes.
                :return: The data without stuffed bytes.
                :rtype: bytearray
        """
        new_frame = bytearray()

        if b'\x7D\x5E' in frame:
            frame = frame.replace(b'\x7D\x5E', b'\x7E')
        if b'\x7D\x5D' in frame:
            frame = frame.replace(b'\x7D\x5D', b'\x7D')
        if b'\x7D\x31' in frame:
            frame = frame.replace(b'\x7D\x31', b'\x11')
        if b'\x7D\x33' in frame:
            frame = frame.replace(b'\x7D\x33', b'\x13')

        return frame

    def read_data(self, _stop_value):
        """add desc"""
        data_to_read = self.ser.inWaiting()
        while data_to_read < _stop_value:
            data_to_read = self.ser.inWaiting()
            time.sleep(0.1)
        data = self.ser.read(data_to_read)

        return data

    @staticmethod
    def segment_miso_frame(miso_frame):
        """add desc"""
        start = miso_frame[0]
        adr = miso_frame[1]
        cmd = miso_frame[2]
        state = miso_frame[3]
        length = miso_frame[4]
        rx_data = miso_frame[5:-2]
        chk = miso_frame[-2]
        stop = miso_frame[-1]

        return start, adr, cmd, state, length, rx_data, chk, stop

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
            pass

        time.sleep(start_up_time)  # Minimum time needed to boot up the sensor.

    def stop_measurement(self):
        """
        Datasheet 5.3.2
        """

        self.ser.write([0x7E, 0x00, 0x01, 0x00, 0xFE, 0x7E])

        if self.debug:
            pass

    def read_measured_values(self, mode='float'):
        """
        Datasheet 5.3.3
        """

        if mode == 'integer':
            stop_value = 27
        else:
            stop_value = 47

        self.ser.reset_input_buffer()  # Clear input buffer to ensure no leftover data in stream.
        self.ser.write([0x7E, 0x00, 0x03, 0x00, 0xFC, 0x7E])  # MOSI

        raw_data = self.read_data(stop_value)  # MISO

        unstuffed_raw_data = self.undo_byte_stuffing(raw_data)  # Undo byte-stuffing in raw_data.

        # Segmenting the MISO Frame.
        start, adr, cmd, state, length, rx_data, chk, stop = self.segment_miso_frame(unstuffed_raw_data)

        # Checking mode to unpack data correctly
        if mode == 'integer':
            try:
                data = struct.unpack(">HHHHHHHHHH", rx_data)  # format = big-endian 10 integers
            except struct.error as e:
                data = [f'Error in unpacking rx_data', rx_data, e]
        else:
            try:
                data = struct.unpack(">ffffffffff", rx_data)  # format = big-endian 10 floats
            except struct.error as e:
                data = [f'Error in unpacking rx_data', rx_data, e]

        return data

    def sleep(self):
        """
        Datasheet 5.3.4
        """

        self.ser.reset_input_buffer()
        self.ser.write([0x7E, 0x00, 0x10, 0x00, 0xEF, 0x7E])

        if self.debug:
            pass

    def wake_up(self):
        """
        Datasheet 5.3.5
        """

        self.ser.reset_input_buffer()
        self.ser.write([0xFF])
        self.ser.write([0x7E, 0x00, 0x11, 0x00, 0xEE, 0x7E])

        if self.debug:
            pass

    def start_fan_cleaning(self):
        """
        Datasheet 5.3.6
        """

        self.ser.reset_input_buffer()
        self.ser.write([0x7E, 0x00, 0x56, 0x00, 0xA9, 0x7E])

        if self.debug:
            pass

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

        # while True:
        #    data_to_read = self.ser.in_waiting()
        #    if data_to_read >= stop_value:
        #        break
        #    time.sleep(0.1)
        # raw_data = self.ser.read(data_to_read)

        raw_data = self.ser.read(stop_value)

        unstuffed_raw_data = self.undo_byte_stuffing(raw_data)  # Unstuffing the raw_data.

        if self.debug:
            pass

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

        raw_data = self.ser.read(stop_value)

        unstuffed_raw_data = self.undo_byte_stuffing(raw_data)  # Unstuffing the raw_data.

        if self.debug:
            pass

        rx_data = unstuffed_raw_data[5:-2]  # Removing header and tail bits.

        try:
            data = struct.unpack(">BBBBBBB", rx_data)  # format = big-endian 7  uint8 integers
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
        stop_value = 12
        raw_data = self.ser.read(stop_value)
        print(raw_data)
        unstuffed_raw_data = self.undo_byte_stuffing(raw_data)

        rx_data = unstuffed_raw_data[5:-2]  # Removing header and tail bits.
        print(rx_data)
        try:
            data = struct.unpack(">LLLLB", rx_data)  # format = big-endian 7  uint8 integers
        except struct.error:
            data = "error in read_version fetch."

    def device_reset(self):
        """
        Datasheet 5.3.11
        """

        self.ser.reset_input_buffer()
        self.ser.write([0x7E, 0x00, 0xD3, 0x00, 0x2C, 0x7E])

        if self.debug:
            pass

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
