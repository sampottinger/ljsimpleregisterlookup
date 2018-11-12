import collections
import copy
import unittest
import json
import os


import lj_device_scribe

from ljm_constants import ljmmm


EXPECTED_TAGS = [u'AIN', u'CORE', u'DAC', u'DIO', u'STREAM', u'SPI', u'I2C', u'ONEWIRE', u'ASYNCH', u'UART', u'LUA', u'AIN_EF', u'TDAC', u'SBUS', u'DIO_EF', u'CONFIG', u'ETHERNET', u'WIFI', u'RTC', u'USER_RAM', u'FILE_IO', u'WATCHDOG', u'INTFLASH']
EXPECTED_REGISTERS = [u'@registers(All TDAC TAGS:):TDAC#(0:22),TDAC_SERIAL_NUMBER,TDAC_SPEED_THROTTLE', u'']
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