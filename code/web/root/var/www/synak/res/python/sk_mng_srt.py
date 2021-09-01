#!/usr/bin/python3

import time

import sk__cmd
import sk__res
import sk__dbg
from sk_mng import *

def process():
  proc_id = getPid()
  try:
    proc_id = int(proc_id)
  except ValueError:
    proc_id = 0
  if proc_id != 0:
    sk__dbg.message(sk__dbg.messtype.NFO, "Master Server already running")
  else:
    sk__cmd.send('sudo tmux new -A -s "synak_ms" -d /synak_ms/synak_ms.bin')
    time.sleep(1.0)
    proc_id = getPid()
    try:
      proc_id = int(proc_id)
    except ValueError:
      proc_id = 0
    if proc_id != 0:
      sk__dbg.message(sk__dbg.messtype.SUC, "Master Server has been started successfully")
    else:
      sk__dbg.message(sk__dbg.messtype.ERR, "Master Server cannot be started")
