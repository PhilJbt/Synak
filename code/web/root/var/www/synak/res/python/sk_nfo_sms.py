#!/usr/bin/python3

import sk__res
import sk__skt
import sk__dbg
from sk_mng import *

# Push segment to client
def prepare(_data):
  ## Get Master Server informations
  dictDataSend = {
    'type' : 'stats'
  }
  arrKeysExpected = [
    'conn',
    'prty'
  ]
  arrTranslate = {
    'conn' : 'Connected players',
    'prty' : 'Games in progress'
  }
  res, err = sk__skt.send(dictDataSend, arrKeysExpected)

  # An error occured (python side), debug message already shown by sk__skt.send()
  if err:
    exit()
  else:
    # An error occured (c++ side)
    if res['type'] == 'erro':
      sk__res.show('erro', res['data'])
    # No error occured
    else:
      ## Get templates
      fTemplate = open("../template/sk_nfo_sms.tpl", "r")
      htmlTemplate = fTemplate.read()
      fStatistics = open("../template/sk_nfo_sms_sta.tpl", "r")
      htmlStatistics = fStatistics.read()
      # Declare all stats concat
      htmlStatsCont = ""

      ## Fill stats template
      # For all stats retrieved from MS
      for key in res['data']:
        htmlStatTemp = htmlStatistics.replace("%NAME%", arrTranslate[key])
        htmlStatTemp = htmlStatTemp.replace("%VALUE%", str(res['data'][key]))
        htmlStatsCont += htmlStatTemp

      ## Fill modal template, and push to client
      htmlTemplate = htmlTemplate.replace("%STATS%", htmlStatsCont)
      sk__res.show("proc", htmlTemplate)
