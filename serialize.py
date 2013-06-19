"""Serialization routines for the Simple Register Lookup project.

Serialization routines to support the web-based Simple Register Lookup project
for LabJack MODBUS devices.

@author Sam Pottinger
@license GNU GPL v2
"""

import copy

DEVICE_MODBUS_MAP_COLS = ["name", "address", "type", "fwmin",
    "read / write", "tags", "description"]


def serialize_device_modbus_map(target):
    """Serializes the given device modbus map to a list of lists.

    This will, for example, take:
    {
        "name": str,
        "address": int,
        "type": str,
        "fwmin": float / int,
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
    ret_list = [DEVICE_MODBUS_MAP_COLS]
    for entry in target:
        entry = copy.deepcopy(entry)
        entry["tags"] = ", ".join(entry["tags"])

        # Serialize read / write values from (bool, bool) to "R", "RW", or "W"
        read_write_str = ""
        if entry["read"]:
            read_write_str += "R"
        if entry["write"]:
            read_write_str += "W"
        entry["read / write"] = read_write_str

        serialized_entry = map(lambda x: entry[x], DEVICE_MODBUS_MAP_COLS)

        ret_list.append(serialized_entry)
    return ret_list
