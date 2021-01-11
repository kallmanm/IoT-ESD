"""
    Supporting functions for sps30
"""


def calculate_checksum(sum_of_bytes):
    """
    The checksum is built before byte-stuffing and checked after removing stuffed bytes from the frame. The checksum
    is defined as follows:
    1. Sum all bytes between start and stop (without start and stop bytes).
    2. Take the least
    significant byte of the result and invert it. This will be the checksum. For a MOSI frame use Address, Command,
    Length and Data to calculate the checksum. For a MISO frame use Address, Command, State, Length and Data to
    calculate the checksum. :param sum: :return checksum:
    """
    checksum = 0xFF - sum_of_bytes
    return checksum
