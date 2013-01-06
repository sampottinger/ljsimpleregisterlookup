import json
import os

import flask

import ljmmm
import serialize


app = flask.Flask(__name__)
app.debug = True
modbus_maps = ljmmm.get_device_modbus_maps()


@app.route("/")
def show_ui():
    return flask.render_template(
        "simple_register_lookup.html",
        device_names = modbus_maps.keys()
    )


@app.route("/lookup/<device_name>.json")
def lookup_device(device_name):
    modbus_map = modbus_maps.get(device_name, None)
    if modbus_map == None:
        flask.abort(404)

    modbus_map_serialized = serialize.serialize_device_modbus_map(modbus_map)
    return json.dumps(modbus_map_serialized)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
