#!/usr/bin/python3

import json

import sk__res
import sk__skt
import sk__dbg

# Push the option modal to the client
def prepare(_data):
    # Get Master Server options values
    dictDataSend = {
      'type' : 'optgt'
    }
    res, err = sk__skt.send(dictDataSend)

    # An error occured (python side), debug message already shown by sk__skt.send()
    if err:
      exit()
    # No error occured
    else:
      # Get the ban modal template
      file = open("../template/sk_mng_optn.tpl", "r")
      template_raw = file.read()

      # Show each changed Synak Master Server option
      template_mod = template_raw.replace("%LGVL%", "\"0\"")

      # Send the modal to the client
      sk__res.show("prep", template_mod)

# Push segment to client
def process(_data):
  # Send Master Server options values
  dictDataSend = {
    'type' : 'optst',
    'data' : json.loads(_data)
  }
  arrTranslate = {
    'lglv' : 'Log level'
  }
  res, err = sk__skt.send(dictDataSend)

  # An error occured (python side), debug message already shown by sk__skt.send()
  if err:
    exit()
  else:
    # An error occured (c++ side)
    if res['type'] == 'erro':
      sk__res.show('erro', res['data'])
    # No error occured
    else:
      # Show each changed Synak Master Server option
      strLine = '<ul class="ui list">'
      for key in res['data']:
        strLine += f"<li><b>{arrTranslate[key]}</b> value has been changed to <b>{str(res['data'][key])}</b></li>"
      strLine += '</ul>'
      sk__dbg.message(sk__dbg.messtype.SUC, strLine)
