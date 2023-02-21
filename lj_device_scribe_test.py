import collections
import copy
import unittest
import json
import os


import lj_device_scribe

from ljm_constants import ljmmm


EXPECTED_TAGS = ['AIN', 'CORE', 'DAC', 'DIO', 'STREAM', 'SPI', 'I2C', 'ONEWIRE', 'ASYNCH', 'UART', 'LUA', 'AIN_EF', 'TDAC', 'SBUS', 'DIO_EF', 'CONFIG', 'ETHERNET', 'WIFI', 'RTC', 'USER_RAM', 'FILE_IO', 'WATCHDOG', 'INTFLASH']
EXPECTED_REGISTERS = ['@registers(All TDAC TAGS:):TDAC#(0:21),TDAC_SERIAL_NUMBER,TDAC_SPEED_THROTTLE', '']
EXPECTED_REGISTERS_EMPTY = ['']


class LJDeviceScribeTests(unittest.TestCase):

    def test_get_all_tags(self):
        tags = lj_device_scribe.get_all_tags()
        self.assertEqual(EXPECTED_TAGS, tags)

    def test_get_registers_for_tag(self):
        tags = lj_device_scribe.get_all_registers_grouped_by_tags("T7", ["TDAC"], ljmmm.get_registers_data(expand_names=False, inc_orig=False))
        self.assertEqual(EXPECTED_REGISTERS, tags)

    def test_empty_tag(self):
        tags = lj_device_scribe.get_all_registers_grouped_by_tags("T4", ["WIFI"], ljmmm.get_registers_data(expand_names=False, inc_orig=False))
        self.assertEqual(EXPECTED_REGISTERS_EMPTY, tags)


if __name__ == "__main__":
    unittest.main()
