#!/usr/bin/python3

import sk__cmd
import sk__res
import sk__dbg
from sk_mng import *

# Push segment to client
def process(_data):
  # Get MS PID
  pid = getPid(True)
  # MS is running, push error message to client
  if pid != 0:
    sk__dbg.message(sk__dbg.messtype.NFO, "Master Server already running")
  # MS is not running
  else:
    # Create a new tmux session, and start a Synak MS instance
    sk__cmd.send('sudo tmux new -A -s "synak_ms" -d /synak_ms/synak_ms.bin')
    # Get MS PID
    pid = getPid(False)
    # One MS process is running, push the success message to client
    if pid != 0:
      sk__dbg.message(sk__dbg.messtype.SUC, "Master Server has been started successfully")
    # No MS process is running, push the error message to client
    else:
      sk__dbg.message(sk__dbg.messtype.ERR, "Master Server cannot be started")
