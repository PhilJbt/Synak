#!/usr/bin/python3

import sys
import json
import subprocess
import os.path

import sk__dbg
import sk__res

def _typeGet(_strType):
  if _strType == 'ERR':
    return ['red', 'exclamation triangle',]
  elif _strType == 'NFO':
    return ['blue', 'info circle',]
  else:
    return ['purple', 'question circle',]

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
        labelParse = _typeGet(lineJson[1])
        lineDesc = '<ul class="ui list">'
        for elem in lineJson[4]:
          lineDesc += f'<li>{elem}</li>'
        lineDesc += '</ul>'
        lineTime = lineJson[3].split(' ')
        lineFile = lineJson[2].split(' ')
        lineModif = htmlItem.replace("%ID%", lineJson[0])
        lineModif = lineModif.replace("%TYPE%", lineJson[1])
        lineModif = lineModif.replace("%CLR1%", labelParse[0])
        lineModif = lineModif.replace("%CLR2%", labelParse[1])
        lineModif = lineModif.replace("%CLR3%", labelParse[1])
        lineModif = lineModif.replace("%FIL1%", lineFile[0])
        lineModif = lineModif.replace("%FIL2%", lineFile[1])
        lineModif = lineModif.replace("%TIM1%", lineTime[0])
        lineModif = lineModif.replace("%TIM2%", lineTime[1])
        lineModif = lineModif.replace("%DESC%", lineDesc)
        lines.append(lineModif)
      strRes = ''.join(lines[::-1])
      htmlLog = htmlLog.replace("%LOG%", strRes)
      sk__res.show("proc", htmlLog)
  # If log file doesn't exist, push an information message to the client
  else:
    sk__dbg.message(sk__dbg.messtype.NFO, "/synak_ms/synak_ms.log file doesn't exist.")
