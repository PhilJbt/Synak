#!/usr/bin/python3

import sk__cmd
import sk__res

def process(_data):
  arrValues = {
  'net.core.rmem_max' : '67108864',
  'net.core.wmem_max' : '67108864',
  'net.core.optmem_max' : '67108864',
  'net.ipv4.tcp_rmem' : '4096 87380 33554432',
  'net.ipv4.tcp_wmem' : '4096 87380 33554432',
  'net.ipv4.tcp_mem' : '1638400 1638400 1638400',
  'net.ipv4.tcp_congestion_control' : 'htcp',
  'net.ipv4.tcp_syncookies' : '1'
  }

  fileRow = open("../template/sk_stt_ded_row.tpl", "r")
  tplRow = fileRow.read()
  strStackedRows = ""
  iErrCount = 0

  for key in arrValues:
    currValue = sk__cmd.send(f'sysctl -n {key}')
    currValue = currValue.strip()
    arrValues[key] = arrValues[key].strip()
    bExpected = bool(arrValues[key] is currValue)
    if bExpected is False:
      iErrCount += 1
    tplRowTemp = tplRow.replace("%NAME%", key)
    tplRowTemp = tplRowTemp.replace("%VALDEF%", arrValues[key])
    tplRowTemp = tplRowTemp.replace("%VALCUR%", currValue)
    tplRowTemp = tplRowTemp.replace("%STATUS%", ('green checkmark' if bExpected is True else 'red attention'))
    tplRowTemp = tplRowTemp.replace("%COLOR%", ('positive' if bExpected is True else 'negative'))
    strStackedRows += tplRowTemp

  #net.core.rmem_max = 67108864
  #net.core.wmem_max = 67108864
  #net.core.optmem_max = 67108864
  #net.ipv4.tcp_rmem = 4096 87380 33554432
  #net.ipv4.tcp_wmem = 4096 65536 33554432
  #max(tcp_wmem) * 2 * 200 / 4096
  #net.ipv4.tcp_mem = 1638400 1638400 1638400
  #net.ipv4.tcp_congestion_control=htcp
  #net.ipv4.tcp_syncookies = 1

  #sysctl -n net.ipv4.tcp_syncookies
  #cat /proc/sys/net/ipv4/tcp_syncookies

  #sudo sysctl -w net.core.rmem_max=$MaxExpectedPathBDP
  #/etc/sysctl.conf
  #sysctl -p

  fileTbl = open("../template/sk_stt_ded_tbl.tpl", "r")
  template_raw = fileTbl.read()
  template_mod = template_raw.replace("%TABLE_COLOR%", ('green' if iErrCount == 0 else 'red'))
  template_mod = template_mod.replace("%VARS_LIST%", strStackedRows)
  template_mod = template_mod.replace("%ERR_COUNT%", (f'{iErrCount} Error' if iErrCount < 2 else f'{iErrCount} Errors'))
  sk__res.show("proc", template_mod)
