#!/usr/bin/python3

import sys
import json
import subprocess
import os.path

import sk__dbg
import sk__res

# Push segment to client
def prepare(_data):
  # If log file exists
  if os.path.isfile('/synak_ms/synak_ms.log'):
    # Read the log file
    res = subprocess.check_output('cat /synak_ms/synak_ms.log', shell=True).decode("utf-8")
    # Replace OS by web new line char
    res = res.replace("\n", "<br/>")
    # If log file is empty, push an information message to the client
    if len(res) == 0:
      sk__dbg.message(sk__dbg.messtype.NFO, "/synak_ms/synak_ms.log file is empty.")
    # If log file exists and is not empty, push the log file to the client
    else:
      sk__res.show("proc", res)
  # If log file doesn't exist, push an information message to the client
  else:
    sk__dbg.message(sk__dbg.messtype.NFO, "/synak_ms/synak_ms.log file doesn't exist.")
