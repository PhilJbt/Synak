#!/usr/bin/python3

import re

import sk__cmd
import sk__res

def process(_data):
  # GET THE PAGE TEMPLATE TEMPLATE
  fileTbl = open("../template/sk_stt_ded_tbl.tpl", "r")
  template_mod = fileTbl.read()


  ## STATS#1
  # GET THE TEMPLATE
  fileSta = open("../template/sk_stt_ded_sta.tpl", "r")
  stat_raw = fileSta.read()

  # FILL WITH HOSTNAME
  info_hst = sk__cmd.send('hostnamectl | grep -iF hostname').strip().split(": ")
  stat_hst = stat_raw.replace("%NAME%", info_hst[0])
  stat_hst = stat_hst.replace("%VALUE%", info_hst[1])

  # FILL WITH OPERATING SYSTEM
  info_lin = sk__cmd.send('hostnamectl | grep -iF operating').strip().split(": ")
  stat_lin = stat_raw.replace("%NAME%", info_lin[0])
  stat_lin = stat_lin.replace("%VALUE%", info_lin[1])

  # FILL WITH ARCHITECTURE
  info_arc = sk__cmd.send('hostnamectl | grep -iF architecture').strip().split(": ")
  stat_arc = stat_raw.replace("%NAME%", info_arc[0])
  stat_arc = stat_arc.replace("%VALUE%", info_arc[1])

  # FILL PAGE TEMPLATE WITH STATS#1
  template_mod = template_mod.replace("%STATS_1%", stat_hst+stat_lin+stat_arc)


  ## STATS#2
  # FILL WITH HDD/SSD USAGE
  info_cpu = str(format(float(sk__cmd.send("awk '/cpu /{print 100*($2+$4)/($2+$4+$5)}' /proc/stat").strip()), '.1f'))
  stat_cpu = stat_raw.replace("%NAME%", "CPU USAGE (%)")
  stat_cpu = stat_cpu.replace("%VALUE%", info_cpu)

  # FILL WITH RAM USAGE
  info_ram = sk__cmd.send("free -m | grep -iF 'mem' | awk '{print $3}'").strip()
  info_ram += "/"
  info_ram += sk__cmd.send("free -m | grep -iF 'mem' | awk '{print $2}'").strip()
  stat_ram = stat_raw.replace("%NAME%", "RAM USAGE (MB)")
  stat_ram = stat_ram.replace("%VALUE%", info_ram)

  # FILL WITH HDD/SSD USAGE
  info_hdd = str(format(float(sk__cmd.send("df --total | grep -iF total | awk '{print $3}'").strip()) / 1e+6, '.1f'))
  info_hdd += "/"
  info_hdd += str(format(float(sk__cmd.send("df --total | grep -iF total | awk '{print $2}'").strip()) / 1e+6, '.1f'))
  stat_hdd = stat_raw.replace("%NAME%", "HDD/SSD USAGE (GB)")
  stat_hdd = stat_hdd.replace("%VALUE%", info_hdd)

  # FILL PAGE TEMPLATE WITH STATS#2
  template_mod = template_mod.replace("%STATS_2%", stat_cpu+stat_ram+stat_hdd)


  ## OPTIMIZATIONS
  # ARRAY WITH OPTIMIZATIONS
  arrValues = {
  'net.core.rmem_max' : '67108864',
  'net.core.wmem_max' : '67108864',
  'net.core.optmem_max' : '67108864',
  'net.ipv4.tcp_rmem' : '4096 87380 33554432',
  'net.ipv4.tcp_wmem' : '4096 87380 33554432',
  'net.ipv4.tcp_mem' : '1638400 1638400 1638400', #max(tcp_wmem) * 2 * 200 / 4096
  'net.ipv4.tcp_congestion_control' : 'bbr',      #https://www.techrepublic.com/article/how-to-enable-tcp-bbr-to-improve-network-speed-on-linux/
  'net.ipv4.tcp_syncookies' : '1'
  }

  # GET THE TABLE TEMPLATE
  fileRow = open("../template/sk_stt_ded_row.tpl", "r")
  tplRow = fileRow.read()
  strStackedRows = ""
  iErrCount = 0

  # FILL THE TABLE TEMPLATE WITH OPTIMIZATIONS
  for key in arrValues:
    currValue = sk__cmd.send(f'sysctl -n {key}')
    currValue = currValue.strip()
    arrValues[key] = arrValues[key].strip()
    bExpected = bool(arrValues[key] == currValue)
    if bExpected is False:
      iErrCount += 1
    tplRowTemp = tplRow.replace("%NAME%", key)
    tplRowTemp = tplRowTemp.replace("%VALDEF%", arrValues[key])
    tplRowTemp = tplRowTemp.replace("%VALCUR%", currValue)
    tplRowTemp = tplRowTemp.replace("%STATUS%", ('green checkmark' if bExpected is True else 'blue question'))
    tplRowTemp = tplRowTemp.replace("%COLOR%", ('positive' if bExpected is True else ''))
    strStackedRows += tplRowTemp

  # REPLACE PAGE TEMPLATE WITH AVAILABLE OPTIMIZATIONS
  template_mod = template_mod.replace("%TABLE_COLOR%", ('green' if iErrCount == 0 else 'blue'))
  template_mod = template_mod.replace("%VARS_LIST%", strStackedRows)
  template_mod = template_mod.replace("%ERR_COUNT%", (f'{iErrCount} optimization available' if iErrCount < 2 else f'{iErrCount} optimizations available'))
  

  ## RETURN HTML
  sk__res.show("proc", template_mod)

  #get val:
  #sysctl -n net.ipv4.tcp_syncookies
  #or:
  #cat /proc/sys/net/ipv4/tcp_syncookies

  #temporary:
  #sudo sysctl -w net.core.rmem_max=$MaxExpectedPathBDP
  #permantent:
  #/etc/sysctl.conf
  #sysctl -p
