"""Serialization routines for the Simple Register Lookup project.

Serialization routines to support the web-based Simple Register Lookup project
for LabJack MODBUS devices.

@author Sam Pottinger
@license GNU GPL v2
"""

import copy

DEVICE_MODBUS_MAP_COLS = [
    # Regular columns
    "name", "address", "type", "access", "tags",

    # detail columns
    "description", "default", "streamable", "isBuffer", "devices", "constants", "altnames", "usesRAM"
]


def serialize_device_modbus_map(target, cols=DEVICE_MODBUS_MAP_COLS):
    """Serializes the given device modbus map to a list of lists.

    This will, for example, take:
    {
        "name": str,
        "address": int,
        "type": str,
        "devices": [
            {
                "device": str,
                "fwmin": float
                "description": str,
                "default": int / float
            }
        ],
        "read": bool,
        "write": bool,
        "tags": list of str,
    }
    and produce
    [str, int, str, int, float / int, str, csv str]
    according to DEVICE_MODBUS_MAP_COLS

    @param target: The device modbus map to serialize in form described in
                   ljmmm.get_device_modbus_maps
    @type target: list of dict
    @return: List of lists with the first list being a header.
    @rtype: list of list
    """
    ret_list = [cols]
    for entry in target:
        entry = copy.deepcopy(entry)
        entry["tags"] = ", ".join(entry["tags"])

        # Serialize read / write values from (bool, bool) to "R", "RW", or "W"
        read_write_str = ""
        if entry["readwrite"]["read"] and entry["readwrite"]["write"]:
            read_write_str = "R / W"
        elif entry["readwrite"]["read"]:
            read_write_str = "R"
        elif entry["readwrite"]["write"]:
            read_write_str = "W"
        entry["access"] = read_write_str

        entry["default"] = entry.get("default", "")

        if len(entry.get("altnames", [])):
            entry["name"] = '%s (also known as: %s)' % (
                entry["name"],
                ", ".join(entry["altnames"])
            )
        else:
            entry["altnames"] = []

        serialized_entry = [entry[x] if x in entry else None for x in cols]

        ret_list.append(serialized_entry)
    return ret_list
