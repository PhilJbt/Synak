#!/usr/bin/python3

import sk__cmd
import sk__res
import sk__dbg
from sk_mng import *

def prepare(_data):
  pid = getPid(False)
  if pid == 0:
    sk__dbg.message(sk__dbg.messtype.NFO, "Master Server is not running")
  else:
    proctree = sk__cmd.send("pstree -a -U -c -n -p | grep synak_ms | grep -v 'grep\|pstree'")
    file = open("../template/sk_mng_kll.tpl", "r")
    template_raw = file.read()
    proctree = proctree.replace('\n', '<br/>')
    template_mod = template_raw.replace("%VAR_1%", proctree)
    sk__res.show("prep", template_mod)

def process(_data):
  pid = getPid(False)
  if pid == 0:
    sk__dbg.message(sk__dbg.messtype.ATT, "It seems that no Master Server was running")
  else:
    sk__cmd.send(f"sudo kill -9 {pid}")
    pid = getPid(True)
    if pid == 0:
      sk__dbg.message(sk__dbg.messtype.SUC, "Master Server has been STOPPED successfully")
    else:
      sk__dbg.message(sk__dbg.messtype.ERR, "Master Server is still running")
