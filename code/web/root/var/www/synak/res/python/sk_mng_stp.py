#!/usr/bin/python3

import time

import sk__cmd
import sk__res
import sk__dbg
from sk_mng import *

def prepare():
  proc_id = getPid()
  try:
    proc_id = int(proc_id)
  except ValueError:
    sk__dbg.message(sk__dbg.messtype.NFO, "Master Server is not running")
  else:
    file = open("../template/sk_mng_stp.tpl", "r")
    template_raw = file.read()
    template_mod = template_raw.replace("%VAR_1%", "test")
    sk__res.show("prep", template_mod)

def process():
  proc_id = getPid()
  try:
    proc_id = int(proc_id)
  except ValueError:
    sk__dbg.message(sk__dbg.messtype.ATT, "It seems that no Master Server was running")
  else:
    sk__cmd.send(f"sudo kill -10  {proc_id}")
    time.sleep(1.0)
    proc_id = getPid()
    try:
      proc_id = int(proc_id)
    except ValueError:
      sk__dbg.message(sk__dbg.messtype.SUC, "Master Server has been stopped successfully")
    else:
      sk__dbg.message(sk__dbg.messtype.ERR, "Master Server is still running")
