#!/usr/bin/python3

import json

import sk__res
import sk__dbg
import sk__dbg


# Push the filled dedicated informations segment to the client
def prepare(_data):
  # Get the Synak Master Server config file (created at startup)
  try:
    cfg_startup = open("/synak_ms/synak_ms.cfg", "r")
    jsn_startup = json.load(cfg_startup)
  except Exception as e:
    sk__dbg.message(sk__dbg.messtype.ERR, f'Synak Master Server config file error ("/synak_ms/synak_ms.cfg", created at startup) : {e}')
    return None, True

  ## Return html
  sk__res.show("proc", "")
