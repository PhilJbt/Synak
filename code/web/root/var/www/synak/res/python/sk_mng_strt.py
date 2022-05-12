#!/usr/bin/python3

import json

import sk__cmd
import sk__res
import sk__dbg
import sk__mng

# Push the modal disclaimer about killing the MS process
def prepare(_data):
  # Get MS PID
  pid = sk__mng.getPid(False)
  # MS is running, push error message to client
  if pid != 0:
    sk__dbg.message(sk__dbg.messtype.NFO, "Master Server is already running")
  # MS is not running
  else:
    # Get the option modal template
    file_raw = open("../template/sk_mng_strt.tpl", "r")
    template_raw = file_raw.read()

    # Get the form modal template
    file_form_global = open("../template/sk_mng_optn_form_global.tpl", "r")
    template_form_global = file_form_global.read()

    # Populate the raw option modal with the option form
    template_mod = template_raw.replace("%FORM_OPT_GLOBAL%", template_form_global)

    # Get the form modal template
    file_form_start = open("../template/sk_mng_optn_form_start.tpl", "r")
    template_form_start = file_form_start.read()

    # Populate the raw option modal with the option form
    template_mod = template_mod.replace("%FORM_OPT_START%", template_form_start)

    # Send the modal to the client
    sk__res.show("prep", template_mod)

# Push segment to client
def process(_data):
  # Get MS PID
  pid = sk__mng.getPid(False)
  # MS is running, push error message to client
  if pid != 0:
    sk__dbg.message(sk__dbg.messtype.ATT, "Master Server is already running")
  # MS process is not running
  else:
    # Create a new tmux session, and start a Synak MS instance
    sk__cmd.send(f'sudo tmux new -A -s "synak_ms" -d /synak_ms/synak_ms.bin "{json.dumps(_data)}"')
    # Get MS PID
    pid = sk__mng.getPid(False)
    # One MS process is running, push the success message to client
    if pid != 0:
      sk__dbg.message(sk__dbg.messtype.SUC, "Master Server has been <b>STARTED</b> successfully")
    # No MS process is running, push the error message to client
    else:
      sk__dbg.message(sk__dbg.messtype.ERR, "Master Server cannot be started")
