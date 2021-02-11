# todo: fix licence
"""
    A python library for control of the Sensirion SPS30 Particulate Matter Sensor.

    All methods from the Sps30 class are designed according to the official datasheet
    provided by Sensirion. The datasheet can be found at the following link:
    https://www.sensirion.com/en/download-center/
    search: sps30, download: Datasheet Particulate Matter Sensors SPS30

    Datasheet Version '1.0 – D1 – March 2020' used in the development of this library.
    Downloaded on 8.1.2021.

    by
    Mattias Kallman
    Github: @kallmanm
    LinkedIn: www.linkedin.com/in/mattias-kallman

    <insert copyright notice>

    <insert LICENSE>

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

import serial
import struct
import time


class Sps30:
    """
    Base class for Sensirion Sps30 Particulate Matter Sensor.
    """

    def __init__(self, port):
        """
        Constructor method for Sps30 class.

        :param string port: Port address.
        """
        self.port = port
        self.ser = serial.Serial(self.port,
                                 baudrate=115200,
                                 bytesize=serial.EIGHTBITS,
                                 stopbits=serial.STOPBITS_ONE,  # This is default class value
                                 parity=serial.PARITY_NONE,  # This is default class value
                                 timeout=2)  # Set at 2 seconds

    @staticmethod
    def calculate_checksum(list_of_bytes):
        """
        Method to calculate the checksum.

        Description of how to calculate the checksum. ref: Datasheet 5.2 Checksum.
        ' The checksum is built before byte-stuffing and checked after removing stuffed bytes from the frame.
        The checksum is defined as follows:
            1. Sum all bytes between start and stop (without start and stop bytes).
            2. Take the least significant byte of the result and invert it. This will be the checksum.
        For a MOSI frame use Address, Command, Length and Data to calculate the checksum.
        For a MISO frame use Address, Command, State, Length and Data to calculate the checksum.'

        :param bytearray list_of_bytes:
        :return byte:
        """
        return 0xFF - sum(list_of_bytes)

    @staticmethod
    def byte_stuffing(frame):
        #TODO: fix
        """
        Method for doing byte-stuffing on a bytearray.

        Datasheet 5.2: Table 5 for details on byte-stuffing.

        :param bytearray frame: The data without stuffed bytes.
        :return bytearray new_frame: The data with stuffed bytes.
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
        # todo: fix desc
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
        # todo: add desc
        """add desc"""
        data_to_read = self.ser.inWaiting()
        while data_to_read < _stop_value:
            data_to_read = self.ser.inWaiting()
            time.sleep(0.1)
        data = self.ser.read(data_to_read)

        return data

    @staticmethod
    def segment_miso_frame(miso_frame):
        # todo: fix desc
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
        # todo: fix desc
        """
        Datasheet 5.3.1
        Measurement Output Format:
        0x03: Big-endian IEEE754 float values
        0x05: Big-endian unsigned 16-bit integer values
        Function default set to Big-endian IEEE754 float values.
        """
        stop_value = 7
        # mode = float cmd
        cmd = [0x7E, 0x00, 0x00, 0x02, 0x01, 0x03, 0xF9, 0x7E]

        if mode == 'integer':
            cmd = [0x7E, 0x00, 0x00, 0x02, 0x01, 0x05, 0xF7, 0x7E]

        self.ser.write(cmd)

        raw_data = self.read_data(stop_value)  # MISO
        unstuffed_raw_data = self.undo_byte_stuffing(raw_data)  # Undo byte-stuffing in raw_data.
        # Segmenting the MISO Frame.
        data = self.segment_miso_frame(unstuffed_raw_data)

        time.sleep(start_up_time)  # Minimum time needed to boot up the sensor. Range: 8 - 30 seconds.

        return data

    def stop_measurement(self):
        # todo: fix desc
        """
        Datasheet 5.3.2
        """
        stop_value = 7
        self.ser.write([0x7E, 0x00, 0x01, 0x00, 0xFE, 0x7E])

        raw_data = self.read_data(stop_value)  # MISO
        unstuffed_raw_data = self.undo_byte_stuffing(raw_data)  # Undo byte-stuffing in raw_data.
        # Segmenting the MISO Frame.
        data = self.segment_miso_frame(unstuffed_raw_data)

        return data

    def read_measured_values(self, mode='float'):
        # todo: fix desc
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
        # todo: fix desc
        """
        Datasheet 5.3.4
        """
        stop_value = 7
        self.ser.reset_input_buffer()
        self.ser.write([0x7E, 0x00, 0x10, 0x00, 0xEF, 0x7E])

        raw_data = self.read_data(stop_value)  # MISO
        unstuffed_raw_data = self.undo_byte_stuffing(raw_data)  # Undo byte-stuffing in raw_data.
        # Segmenting the MISO Frame.
        data = self.segment_miso_frame(unstuffed_raw_data)

        return data

    def wake_up(self):
        # todo: fix desc
        """
        Datasheet 5.3.5
        """
        stop_value = 7
        self.ser.reset_input_buffer()
        self.ser.write([0xFF])
        self.ser.write([0x7E, 0x00, 0x11, 0x00, 0xEE, 0x7E])

        raw_data = self.read_data(stop_value)  # MISO
        unstuffed_raw_data = self.undo_byte_stuffing(raw_data)  # Undo byte-stuffing in raw_data.
        # Segmenting the MISO Frame.
        data = self.segment_miso_frame(unstuffed_raw_data)

        return data

    def start_fan_cleaning(self):
        # todo: fix desc
        """
        Datasheet 5.3.6
        """
        stop_value = 7
        self.ser.reset_input_buffer()
        self.ser.write([0x7E, 0x00, 0x56, 0x00, 0xA9, 0x7E])

        raw_data = self.read_data(stop_value)  # MISO
        unstuffed_raw_data = self.undo_byte_stuffing(raw_data)  # Undo byte-stuffing in raw_data.
        # Segmenting the MISO Frame.
        data = self.segment_miso_frame(unstuffed_raw_data)

        return data

    def read_write_auto_cleaning_interval(self):
        """
        Datasheet 5.3.7
        """

        # self.ser.reset_input_buffer()
        # Read Auto Cleaning Interval:
        # self.ser.write([0x7E, 0x00, 0x80, 0x01, 0x00, 0x7D, 0x5E, 0x7E])
        # Write Auto Cleaning Interval to 0 (disable):
        # Disabled, use with caution.
        # self.ser.write([0x7E, 0x00, 0x80, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7A, 0x7E])
        return 'NOT IMPLEMENTED'

    def device_information(self, return_info='product_type'):
        # todo: fix desc
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

        raw_data = self.ser.read(stop_value)  # MISO
        unstuffed_raw_data = self.undo_byte_stuffing(raw_data)  # Undo byte-stuffing in raw_data.
        # Segmenting the MISO Frame.
        start, adr, cmd, state, length, rx_data, chk, stop = self.segment_miso_frame(unstuffed_raw_data)

        data = rx_data.decode('ascii')

        return data

    def read_version(self):
        # todo: fix desc
        """
        Datasheet 5.3.9
        """

        stop_value = 14
        self.ser.reset_input_buffer()
        self.ser.write([0x7E, 0x00, 0xD1, 0x00, 0x2E, 0x7E])

        raw_data = self.read_data(stop_value)  # MISO
        unstuffed_raw_data = self.undo_byte_stuffing(raw_data)  # Undo byte-stuffing in raw_data.
        # Segmenting the MISO Frame.
        start, adr, cmd, state, length, rx_data, chk, stop = self.segment_miso_frame(unstuffed_raw_data)

        try:
            data = struct.unpack(">BBBBBBB", rx_data)  # format = big-endian 7  uint8 integers
        except struct.error as e:
            data = e

        return data

    def read_device_status_register(self):
        # todo: fix desc
        """
        Datasheet 5.3.10
        """
        stop_value = 12
        self.ser.reset_input_buffer()
        self.ser.write([0x7E, 0x00, 0xD2, 0x01, 0x00, 0x2C, 0x7E])

        raw_data = self.read_data(stop_value)  # MISO
        unstuffed_raw_data = self.undo_byte_stuffing(raw_data)  # Undo byte-stuffing in raw_data.
        # Segmenting the MISO Frame.
        data = self.segment_miso_frame(unstuffed_raw_data)

        return data

    def device_reset(self):
        # todo: fix desc
        """
        Datasheet 5.3.11
        """
        stop_value = 7
        self.ser.reset_input_buffer()
        self.ser.write([0x7E, 0x00, 0xD3, 0x00, 0x2C, 0x7E])

        raw_data = self.read_data(stop_value)  # MISO
        unstuffed_raw_data = self.undo_byte_stuffing(raw_data)  # Undo byte-stuffing in raw_data.
        # Segmenting the MISO Frame.
        data = self.segment_miso_frame(unstuffed_raw_data)

        return data

    def open_port(self):
        # todo: fix desc
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
        # todo: fix desc
        """
        Closes the port connection immediately.
        """

        self.ser.close()
