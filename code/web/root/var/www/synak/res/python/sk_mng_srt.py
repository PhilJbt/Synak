#!/usr/bin/python3

import sk__cmd
import sk__res
import sk__dbg
from sk_mng import *

def process(_data):
  pid = getPid(True)
  if pid > 0:
    sk__dbg.message(sk__dbg.messtype.NFO, "Master Server already running")
  else:
    sk__cmd.send('sudo tmux new -A -s "synak_ms" -d /synak_ms/synak_ms.bin')
    pid = getPid(False)
    if pid > 0:
      sk__dbg.message(sk__dbg.messtype.SUC, "Master Server has been started successfully")
    else:
      sk__dbg.message(sk__dbg.messtype.ERR, "Master Server cannot be started")
