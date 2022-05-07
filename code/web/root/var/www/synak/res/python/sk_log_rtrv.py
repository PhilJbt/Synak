#!/usr/bin/python3

import sys
import json
import subprocess
import os.path

import sk__dbg
import sk__res

def _typeGet(_strType):
  if _strType == '[START]':
    return 'grey play circle outline'
  elif _strType == '[STOP]':
    return 'grey stop circle outline'
  elif _strType == '[ERROR]':
    return 'red exclamation triangle'
  elif _strType == '[INFO]':
    return 'blue info circle'
  else:
    return 'purple question circle'

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
      # Replace brackets by HTML label tags
      strRes = '<div class="ui feed large">'
      for line in res.splitlines():
        iEndCode = line.find(']') + 1
        strCode  = line[1:iEndCode-1].replace('::', ' (') + ')'
        iEndType = line[iEndCode:].find(']') + 1
        strType  = line[iEndCode + 1:iEndCode + iEndType]
        strDesc  = line[iEndCode + iEndType:]
        strRes += f'<div class="event">\
                      <div class="label">\
                        <i class="icon {_typeGet(strType)}"></i>\
                      </div>\
                      <div class="content">\
                        <div class="summary">\
                          {strDesc}\
                        </div>\
                        <div class="meta">\
                          <div class="like">\
                            {strCode}\
                          </div>\
                        </div>\
                      </div>\
                    </div>'
      strRes += '</div>'
      sk__res.show("proc", strRes)
  # If log file doesn't exist, push an information message to the client
  else:
    sk__dbg.message(sk__dbg.messtype.NFO, "/synak_ms/synak_ms.log file doesn't exist.")
