#!/usr/bin/python3

import sk__cmd
import sk__res
import sk__dbg
from sk_mng import *

def prepare():
  pid = getPid(False)
  if pid == 0:
    sk__dbg.message(sk__dbg.messtype.NFO, "Master Server is not running")
  else:
    file = open("../template/sk_mng_stp.tpl", "r")
    template_raw = file.read()
    sk__res.show("prep", template_raw)

def process():
  pid = getPid(False)
  if pid == 0:
    sk__dbg.message(sk__dbg.messtype.ATT, "It seems that no Master Server was running")
  else:
    sk__cmd.send(f"sudo kill -10 {pid}")
    pid = getPid(True)
    if pid == 0:
      sk__dbg.message(sk__dbg.messtype.SUC, "Master Server has been KILLED successfully")
    else:
      sk__dbg.message(sk__dbg.messtype.ERR, "Master Server is still running")
