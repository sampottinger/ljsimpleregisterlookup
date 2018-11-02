import json
from ljm_constants import ljmmm

def get_all_register_grouped_by_tags(device, tags, data):
    data = json.loads(json.dumps(data))
    registers = {}
    alltags = False
    for tag in tags:
        if(tag == "ALL_TAGS_NAME"):
            tags = "AIN, AIN_EF, ASYNCH, CONFIG, CORE, DAC, DIO, DIO_EF, ETHERNET, FILE_IO, I2C, INTFLASH, LUA, ONEWIRE, RTC, SBUS, SPI, STREAM, TDAC, UART, USER_RAM, WATCHDOG, WIFI"
            tags = tags.replace(" ","").split(',')
            return get_all_register_grouped_by_tags(device, tags, data)
            break
        registers[tag]=[]
    for x in data:
        for c in x['devices']:
            if(c['device'] == device):
                for t in x['tags']:
                    for b in tags:
                        if(t == b):
                            registers[b].append(x["name"])
    return render_get_all_register_grouped_by_tags(json.loads(json.dumps(registers)))


def render_get_all_register_grouped_by_tags(tagdata):
    devicegroup=""
    for x in tagdata:
        if(len(tagdata[x])>0):
            devicegroup += '@registers(All ' + x + ' TAGS:):' + json.dumps(tagdata[x]).replace(" ","").replace('"',"").replace(']',"").replace('[',"")+ "/"
    return devicegroup.split('/')
