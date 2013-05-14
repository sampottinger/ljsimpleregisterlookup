"""Tests for serializing modbus information for Simple Register Lookup.

@author Sam Pottinger
@license GNU GPL v2
"""

import unittest

import serialize


# TODO: This is still somewhat incomplete
class SerializeTests(unittest.TestCase):
    """Test case for reading LabJack Modbus Map Markup notation maps."""

    def test_serialize_device_modbus_map(self):
        """Test serializing a modbus map for a single device."""
        test_modbus_map = [
            {
                "name": "test_1",
                "address": 1,
                "type": "UINT16",
                "numregs": 1,
                "fwmin": 0,
                "read": True,
                "write": False,
                "tags": ["tag1", "tag2"],
            },
            {
                "name": "test_2",
                "address": 2,
                "type": "UINT16",
                "numregs": 1,
                "fwmin": 0,
                "read": False,
                "write": True,
                "tags": ["tag3", "tag4"],
            }
        ]
        expected = [
            [
                "name",
                "address",
                "type",
                "fwmin",
                "read",
                "write",
                "tags"
            ],
            [
                "test_1",
                1,
                "UINT16",
                0,
                True,
                False,
                "tag1, tag2"
            ],
            [
                "test_2",
                2,
                "UINT16",
                0,
                False,
                True,
                "tag3, tag4"
            ]
        ]

        serialized = serialize.serialize_device_modbus_map(test_modbus_map)
        self.assertListEqual(serialized, expected)


if __name__ == '__main__':
    unittest.main()