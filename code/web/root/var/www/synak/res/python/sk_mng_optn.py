#!/usr/bin/python3

import json

import sk__res
import sk__skt
import sk__dbg

# Push the option modal to the client
def prepare(_data):
    # Get Master Server options values
    dictDataSend = {
        'type' : 'optgt'
    }
    res, err = sk__skt.send(dictDataSend)

    # No error occured
    if not err:
        # Get the option modal template
        file_raw = open("../template/sk_mng_optn.tpl", "r")
        template_raw = file_raw.read()

        # Replace the default value of the log level option
        template_mod = template_raw.replace("%LGLV%", f'''"{res['data']['lglv']}"''')

        # Get the form modal template
        file_form = open("../template/sk_mng_optn_form_global.tpl", "r")
        template_form = file_form.read()

        # Populate the raw option modal with the option form
        template_mod = template_mod.replace("%FORM_OPT_GLOBAL%", template_form)

        # Send the modal to the client
        sk__res.show("prep", template_mod)

# Push segment to client
def process(_data):
    # Send Master Server options values
    dictDataSend = {
        'type' : 'optst',
        'data' : json.loads(_data)
    }
    arrTranslate = {
        'lglv' : 'Log level'
    }
    res, err = sk__skt.send(dictDataSend)

    # No error occured
    if not err:
        # Show each changed Synak Master Server option
        strLine = '<ul class="ui list">'
        for key in res['data']:
            strLine += f"<li><b>{arrTranslate[key]}</b> value has been changed to <b>{str(res['data'][key])}</b></li>"
        strLine += '</ul>'
        sk__dbg.message(sk__dbg.messtype.SUC, strLine)
