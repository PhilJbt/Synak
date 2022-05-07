#!/usr/bin/python3

import sys
import json
import subprocess
import os.path

import sk__dbg
import sk__res

def _typeGet(_strType):
  typeIndentifier = _strType[0:1]
  if typeIndentifier == 'E':
    return ['red', 'exclamation triangle', 'exclamation triangle']
  if typeIndentifier == 'N':
    if _strType == 'NFO_100':
      return ['blue', 'play circle', 'play circle']
    elif _strType == 'NFO_101':
      return ['blue', 'stop circle', 'stop circle']
    else:
      return ['blue', 'info circle', 'info circle']
  else:
    return ['purple', 'question circle', 'question circle']

# Push the filled log html segment to the client
def prepare(_data):
  # If log file exists
  if os.path.isfile('/synak_ms/synak_ms.log'):
    # Read the log file
    res = subprocess.check_output('cat /synak_ms/synak_ms.log', shell=True).decode("utf-8")
    # If log file is empty, push an information message to the client
    if len(res) < 5:
      sk__dbg.message(sk__dbg.messtype.NFO, "/synak_ms/synak_ms.log file is empty.")
    # If log file exists and is not empty, push the log file to the client
    else:
      # Get the log template
      fileLog = open("../template/sk_log_rtv.tpl", "r")
      htmlLog = fileLog.read()
      # Get the log item template
      fileItem = open("../template/sk_log_rtv_itm.tpl", "r")
      htmlItem = fileItem.read()
      # Replace brackets by HTML label tags
      lines = []
      for line in res.splitlines():
        lineJson = json.loads(line)
        timeParse = lineJson[2].split(' ')
        labelParse = _typeGet(lineJson[0])
        lineModif = htmlItem.replace("%ERI1%", labelParse[0])
        lineModif = lineModif.replace("%ERI2%", labelParse[1])
        lineModif = lineModif.replace("%ERI3%", labelParse[2])
        lineModif = lineModif.replace("%ERCD%", lineJson[0])
        lineModif = lineModif.replace("%FILE%", lineJson[1])
        lineModif = lineModif.replace("%TMEH%", timeParse[0])
        lineModif = lineModif.replace("%TMED%", timeParse[1])
        lineModif = lineModif.replace("%DESC%", lineJson[3])
        lines.append(lineModif)
      strRes = ''.join(lines[::-1])
      htmlLog = htmlLog.replace("%LOG%", strRes)
      sk__res.show("proc", htmlLog)
  # If log file doesn't exist, push an information message to the client
  else:
    sk__dbg.message(sk__dbg.messtype.NFO, "/synak_ms/synak_ms.log file doesn't exist.")
