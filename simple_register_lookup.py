"""Simple Modbus Map register lookup web application.

@author Sam Pottinger
@license GNU GPL v2
"""

import json
import os

import flask

import ljmmm
import serialize


app = flask.Flask(__name__)
modbus_maps = ljmmm.get_device_modbus_maps()
ALL_DEVICES_NAME = 'All Devices'


@app.route("/")
def show_ui():
    """Display the JavaScript client for viewing MODBUS map information."""
    device_options = modbus_maps.keys()
    # TODO: add tags
    device_options.insert(0, ALL_DEVICES_NAME)
    return flask.render_template(
        "simple_register_lookup.html",
        device_names = device_options
    )


@app.route("/lookup/<device_name>.json",
    defaults={'tag': None, 'reg_name': None, 'not_tag': None})

@app.route("/lookup/tag=<tag>",
    defaults={'device_name': ALL_DEVICES_NAME, 'reg_name': None, 'not_tag': None})

@app.route("/lookup/tag=<tag>&not_tag=<not_tag>",
    defaults={'device_name': ALL_DEVICES_NAME, 'reg_name': None})

@app.route("/lookup/reg_name=<reg_name>",
    defaults={'device_name': ALL_DEVICES_NAME, 'tag': None, 'not_tag': None})

def lookup_device(device_name, reg_name, tag, not_tag):
    """Render JSON formatted device MODBUS map."""
    modbus_map = []
    if device_name == ALL_DEVICES_NAME:
        for device_name in modbus_maps.keys():
            modbus_map.extend(modbus_maps.get(device_name, None))

        modbus_map = uniques(modbus_map)

    else:
        modbus_map = modbus_maps.get(device_name, None)

    if modbus_map == None:
        flask.abort(404)

    # TODO: fix Horrible style here
    # TODO: Set defaults to "None" instead of None
    if tag:
        temp = []
        for entry in modbus_map:
            for map_tag in entry['tags']:
                if map_tag.find(unicode(tag)) != -1:
                    temp.append(entry)

        modbus_map = temp

    if not_tag:
        entries_to_remove = []
        for entry in modbus_map:
            for map_tag in entry['tags']:
                if map_tag.find(unicode(not_tag)) != -1:
                    entries_to_remove.append(entry)

        for entry in entries_to_remove:
            modbus_map.remove(entry)

    if reg_name:
        temp = []
        for entry in modbus_map:
            map_name = entry['name']
            if map_name.find(unicode(reg_name)) != -1:
                temp.append(entry)

        modbus_map = temp

    modbus_map_serialized = serialize.serialize_device_modbus_map(modbus_map)
    response = flask.make_response(json.dumps(modbus_map_serialized))
    response.headers["X-XSS-Protection"] = "0"
    response.headers["Access-Control-Allow-Origin"] = "http://labjack.com"
    return response

# Thanks http://www.peterbe.com/plog/uniqifiers-benchmark
def uniques(seq, idfun=None):
   # order preserving
   if idfun is None:
       def idfun(x): return x['name']
   seen = {}
   result = []
   for item in seq:
       marker = idfun(item)
       # in old Python versions:
       # if seen.has_key(marker)
       # but in new ones:
       if marker in seen: continue
       seen[marker] = 1
       result.append(item)
   return result


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
