#!/usr/bin/python3

import json

import sk__res
import sk__skt
import sk__dbg
import sk__opn

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
        template_raw = sk__opn.getTemplate("sk_mng_optn")

        # Replace the default value of the log level option
        template_mod = template_raw.replace("%LGLV%", f'''"{res['data']['lglv']}"''')

        # Get the form modal template
        template_form = sk__opn.getTemplate("sk_mng_optn_form_global")

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
