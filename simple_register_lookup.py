"""Simple Modbus Map register lookup web application.

@author Sam Pottinger
@license GNU GPL v2
"""

import json
import os

import flask
from flask import Markup, request

import ljmmm
import serialize


app = flask.Flask(__name__)
modbus_maps = ljmmm.get_device_modbus_maps()
ALL_DEVICES_NAME = 'All Devices'
ALL_TAGS_NAME = 'All Tags'
# NO_TAGS_NAME = 'No Tags'


@app.route("/")
def show_ui():
    """Display the JavaScript client for viewing MODBUS map information."""

    # Until these devices are supported, we should remove them to avoid confusing anyone
    def safe_remove(d, item):
        if d.get(item, None):
            del d[item]
    safe_remove(modbus_maps, 'UE9')
    safe_remove(modbus_maps, 'U6')
    safe_remove(modbus_maps, 'U3')

    device_options = modbus_maps.keys()
    device_options.insert(0, ALL_DEVICES_NAME)

    tag_options = set()
    for x in modbus_maps:
        for reg in modbus_maps[x]:
            for tag in reg['tags']:
                tag_options.add(tag)
    tag_options = sorted(list(filter(None, tag_options)))

    tag_options = [Markup('<option value="{tag}">{tag}</option>').format(tag=tag)
        for tag in tag_options]

    # not_tag_options = list(tag_options)
    # not_tag_options.insert(0, '<option value="{not_tag}" selected="selected">{not_tag}</option>'.
    #     format(not_tag=NO_TAGS_NAME))

    tag_options.insert(0,
        '<option value="{tag}" selected="selected">{tag}</option>'.format(tag=ALL_TAGS_NAME))


    return flask.render_template(
        "simple_register_lookup.html",
        device_names = device_options,
        tags = tag_options
    )

invalid_arguments = ['null', 'undefined']
def filterArg(argument):
    if argument in invalid_arguments:
        return []

    return argument.split(',')

@app.route('/lookup.json')
def lookup():
    """Render JSON formatted device MODBUS map."""

    device_name = request.args.get("device_name", ALL_DEVICES_NAME)
    tags = filterArg(request.args.get("tags", ALL_TAGS_NAME))
    not_tags = filterArg(request.args.get("not-tags", "null"))
    add_reg_names = filterArg(request.args.get("add-reg-names", "null"))

    if device_name in invalid_arguments:
        device_name = ALL_DEVICES_NAME

    modbus_map = []
    if device_name == ALL_DEVICES_NAME:
        for device_name in modbus_maps.keys():
            modbus_map.extend(modbus_maps.get(device_name, None))

        modbus_map = uniques(modbus_map)

    else:
        modbus_map = modbus_maps.get(device_name, None)

    if modbus_map == None:
        flask.abort(404)

    # Pre filter
    unfiltered_registers = []
    if add_reg_names:
        for entry in modbus_map:
            for rn in add_reg_names:

                # This should probably be == instead, but url params don't like the #(0:1) stuff
                if unicode(rn) in unicode(entry['name']):
                    unfiltered_registers.append(entry)

    # Filter by tag
    if tags and unicode(ALL_TAGS_NAME) not in tags:
        temp = []
        for entry in modbus_map:
            for map_tag in entry['tags']:
                for t in tags:
                    if map_tag.find(unicode(t)) != -1:
                        temp.append(entry)

        modbus_map = temp

    # Filter by not-tag
    if not_tags: # and unicode(NO_TAGS_NAME) not in not_tags:
        entries_to_remove = []
        for entry in modbus_map:
            for map_tag in entry['tags']:
                for nt in not_tags:
                    if map_tag.find(unicode(nt)) != -1:
                        entries_to_remove.append(entry)

        for entry in entries_to_remove:
            modbus_map.remove(entry)

    # Add the pre-filter contents
    for unfiltered_reg in unfiltered_registers:
        duplicate = False
        for reg in modbus_map:
            if unicode(unfiltered_reg['name']) == unicode(reg['name']):
                duplicate = True

        if not duplicate:
            modbus_map.append(unfiltered_reg)

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
