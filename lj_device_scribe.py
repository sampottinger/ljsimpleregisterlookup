import json
from ljm_constants import ljmmm

def get_all_tags():
    tags = ""
    tagjson = ljmmm.get_registers_data(expand_names=False, inc_orig=False)
    for register in tagjson:
        for tag in register["tags"]:
            if(tag not in tags):
                tags += tag + ","
    return tags[:-1].replace(" ","").split(',')

alltags_list = get_all_tags()
def sanitize_get_all_registers_grouped_by_tags(rawdata):
    return json.loads(json.dumps(rawdata))

def get_all_registers_grouped_by_tags(device, tags, data):
    data = sanitize_get_all_registers_grouped_by_tags(data)
    registers = {}
    alltags = False
    for tag in tags:
        if(tag == "ALL_TAGS_NAME"):
            tags = alltags_list
            return get_all_registers_grouped_by_tags(device, tags, data)
        registers[tag]=[]
    for x in data:
        for c in x['devices']:
            if(c['device'] == device):
                for t in x['tags']:
                    for b in tags:
                        if(t == b):
                            registers[b].append(x["name"])
    return render_get_all_registers_grouped_by_tags(sanitize_get_all_registers_grouped_by_tags(registers))


def render_get_all_registers_grouped_by_tags(tagdata):
    devicegroup=""
    for x in tagdata:
        if(len(tagdata[x])>0):
            devicegroup += '@registers(All ' + x + ' TAGS:):' + json.dumps(tagdata[x]).replace(" ","").replace('"',"").replace(']',"").replace('[',"")+ "/"
    return devicegroup.split('/')
