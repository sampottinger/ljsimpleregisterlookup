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
                "readwrite": {
                    "read": True,
                    "write": False
                },
                "tags": ["tag1", "tag2"],
                "description": "test1"
            },
            {
                "name": "test_2",
                "address": 2,
                "type": "UINT16",
                "numregs": 1,
                "fwmin": 0,
                "readwrite": {
                    "read": False,
                    "write": True
                },
                "tags": ["tag3", "tag4"],
                "description": "test2",
                "altnames": ["alternate_name"],
            }
        ]
        expected = [
            [
                "name",
                "address",
                "type",
                "access",
                "tags",
                "description",
                "default",
                "streamable",
                "isBuffer",
                "devices",
                "constants",
                "altnames",
            ],
            [
                "test_1",
                1,
                "UINT16",
                "R",
                "tag1, tag2",
                "test1",
                "",
                None,
                None,
                None,
                None,
                [],
            ],
            [
                "test_2 (also known as: alternate_name)",
                2,
                "UINT16",
                "W",
                "tag3, tag4",
                "test2",
                "",
                None,
                None,
                None,
                None,
                ['alternate_name']
            ]
        ]

        serialized = serialize.serialize_device_modbus_map(test_modbus_map)
        self.assertListEqual(serialized, expected)


if __name__ == '__main__':
    unittest.main()