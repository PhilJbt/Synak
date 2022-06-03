#!/usr/bin/python3

import json
import os.path

import sk__cmd
import sk__res
import sk__dbg
import sk__mng
import sk__opn

# Push the modal disclaimer about killing the MS process
def prepare(_data):
    # Get MS PID
    pid = sk__mng.getPid(True)
    # MS is running, push error message to client
    if pid != 0:
        sk__dbg.message(sk__dbg.messtype.NFO, "Master Server is already running")
    # MS is not running
    else:
        # Get the option modal template
        template_raw = sk__opn.getTemplate("sk_mng_strt")

        # Get the form modal template
        template_form_global = sk__opn.getTemplate("sk_mng_optn_form_global")

        # Populate the raw option modal with the option form
        template_mod = template_raw.replace("%FORM_OPT_GLOBAL%", template_form_global)

        # Get the form modal template
        template_form_start = sk__opn.getTemplate("sk_mng_optn_form_start")

        # Populate the raw option modal with the option form
        template_mod = template_mod.replace("%FORM_OPT_START%", template_form_start)

        # Try to get last configuration
        portWP = '45318'
        portPL = '45350'
        logLvl = '3'
        if os.path.exists('/synak_ms/synak_ms.cfg'):
            try:
                cfg_startup = open("/synak_ms/synak_ms.cfg", "r")
                jsn_startup = json.load(cfg_startup)
                portWP = jsn_startup['ptwp']
                portPL = jsn_startup['ptpl']
                logLvl = jsn_startup['lglv']
            except:
                portWP = '45318'
                portPL = '45350'
                logLvl = '3'

        # Populate values with last configuration (or default)
        template_mod = template_mod.replace("%portWP%", portWP)
        template_mod = template_mod.replace("%portPL%", portPL)
        template_mod = template_mod.replace("%LOGLEVEL%", logLvl)

        # Send the modal to the client
        sk__res.show("prep", template_mod)

# Push segment to client
def process(_data):
    # Get MS PID
    pid = sk__mng.getPid(True)
    # MS is running, push error message to client
    if pid != 0:
        sk__dbg.message(sk__dbg.messtype.ATT, "Master Server is already running")
    # MS process is not running
    else:
        # Create a new tmux session, and start a Synak MS instance
        chk, res = sk__cmd.send(f'sudo tmux new -A -s "synak_ms" -d /synak_ms/synak_ms.bin "{json.dumps(_data)}"')
        if chk == False:
            return
        # Get MS PID
        pid = sk__mng.getPid(True)
        # One MS process is running, push the success message to client
        if pid != 0:
            sk__dbg.message(sk__dbg.messtype.SUC, "Master Server has been <b>STARTED</b> successfully")
        # No MS process is running, push the error message to client
        else:
            sk__dbg.message(sk__dbg.messtype.ERR, "Master Server cannot be started")
