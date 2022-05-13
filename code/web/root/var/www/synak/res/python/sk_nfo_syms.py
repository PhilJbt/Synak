#!/usr/bin/python3

import sk__res
import sk__skt
import sk__dbg

# Push the filled Synak MS informations segment to the client
def prepare(_data):
    # Get Master Server informations
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

    # No error occured
    if not err:
        ## Get templates
        fTemplate = open("../template/sk_nfo_syms.tpl", "r")
        htmlTemplate = fTemplate.read()
        fStatistics = open("../template/sk_nfo_syms_sta.tpl", "r")
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
