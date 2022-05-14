#!/usr/bin/python3

import json
import os.path

import sk__res
import sk__dbg
import sk__dbg
import sk__opn

# Push the filled dedicated informations segment to the client
def prepare(_data):
    if os.path.exists('/synak_ms/synak_ms.cfg'):
        # Get the Synak Master Server config file (created at startup)
        try:
            cfg_startup = open("/synak_ms/synak_ms.cfg", "r")
            jsn_startup = json.load(cfg_startup)
        except Exception as e:
            sk__dbg.message(sk__dbg.messtype.ERR, f'Synak Master Server config file error ("/synak_ms/synak_ms.cfg", created at startup) : {e}')
            return None, True

        # Get the config html template
        template_raw = sk__opn.getTemplate("sk_nfo_cnfg")

        # Format user readable Log Level
        strLogLevel = ''
        if jsn_startup['lglv'] == '0' :
            strLogLevel = '<i class="icon info circle blue"></i> Informations'
        elif jsn_startup['lglv'] == '1' :
            strLogLevel = '<i class="icon exclamation circle orange"></i> Warnings'
        else:
            strLogLevel = '<i class="icon exclamation triangle red"></i> Errors'

        # Replace value with those of the configuration file
        template_mod = template_raw.replace("%PTWP%", jsn_startup['ptwp'])
        template_mod = template_mod.replace("%PTPL%", jsn_startup['ptpl'])
        template_mod = template_mod.replace("%LGLV%", strLogLevel)

        # Return html
        sk__res.show("proc", template_mod)
    else:
        sk__dbg.message(sk__dbg.messtype.ERR, 'Log file "/synak_ms/synak_ms.cfg" does not exist.')
