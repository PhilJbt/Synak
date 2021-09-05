#!/usr/bin/python3

import re

import sk__cmd
import sk__res

# Push dedicated informations segment to the client
def process(_data):
  # Get the page template template
  fileTbl = open("../template/sk_nfo_ded_tbl.tpl", "r")
  template_mod = fileTbl.read()


  ## Stats#1
  # Get the template
  fileSta = open("../template/sk_nfo_ded_sta.tpl", "r")
  stat_raw = fileSta.read()

  # Fill stats#1 with hostname
  info_hst = sk__cmd.send('hostnamectl | grep -iF hostname').strip().split(": ")
  stat_hst = stat_raw.replace("%NAME%", info_hst[0])
  stat_hst = stat_hst.replace("%VALUE%", info_hst[1])

  # Fill stats#1 with operating system
  info_lin = sk__cmd.send('hostnamectl | grep -iF operating').strip().split(": ")
  stat_lin = stat_raw.replace("%NAME%", info_lin[0])
  stat_lin = stat_lin.replace("%VALUE%", info_lin[1])

  # Fill stats#1 with architecture
  info_arc = sk__cmd.send('hostnamectl | grep -iF architecture').strip().split(": ")
  stat_arc = stat_raw.replace("%NAME%", info_arc[0])
  stat_arc = stat_arc.replace("%VALUE%", info_arc[1])

  # Fill stats#1 page template with stats#1
  template_mod = template_mod.replace("%STATS_1%", stat_hst+stat_lin+stat_arc)


  ## Stats#2
  # Fill stats#2 with hdd/ssd usage
  info_cpu = format(float(sk__cmd.send('top -b -d1 -n1|grep -i "Cpu(s)"|head -c21|awk \'{print $2}\'').strip()), '.1f')
  if float(info_cpu) < 0.1:
    info_cpu = '0.1'
  stat_cpu = stat_raw.replace("%NAME%", "CPU USAGE (%)")
  stat_cpu = stat_cpu.replace("%VALUE%", str(info_cpu))

  # Fill stats#2 with ram usage
  info_ram = sk__cmd.send("free -m | grep -iF 'mem' | awk '{print $3}'").strip()
  info_ram += "/"
  info_ram += sk__cmd.send("free -m | grep -iF 'mem' | awk '{print $2}'").strip()
  stat_ram = stat_raw.replace("%NAME%", "RAM USAGE (MB)")
  stat_ram = stat_ram.replace("%VALUE%", info_ram)

  # Fill stats#2 with hdd/ssd usage
  info_hdd = str(format(float(sk__cmd.send("df --total | grep -iF total | awk '{print $3}'").strip()) / 1e+6, '.1f'))
  info_hdd += "/"
  info_hdd += str(format(float(sk__cmd.send("df --total | grep -iF total | awk '{print $2}'").strip()) / 1e+6, '.1f'))
  stat_hdd = stat_raw.replace("%NAME%", "HDD/SSD USAGE (GB)")
  stat_hdd = stat_hdd.replace("%VALUE%", info_hdd)

  # Fill stats#2 page template with stats#2
  template_mod = template_mod.replace("%STATS_2%", stat_cpu+stat_ram+stat_hdd)


  ## Optimizations
  # Array with optimizations
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

  # Get the table template
  fileRow = open("../template/sk_nfo_ded_row.tpl", "r")
  tplRow = fileRow.read()
  strStackedRows = ""
  iErrCount = 0

  # Fill the table template with optimizations
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
    tplRowTemp = tplRowTemp.replace("%STATUS%", ('green checkmark' if bExpected is True else 'yellow exclamation triangle'))
    tplRowTemp = tplRowTemp.replace("%COLOR%", ('positive' if bExpected is True else ''))
    strStackedRows += tplRowTemp

  # Replace page template with available optimizations
  template_mod = template_mod.replace("%TABLE_COLOR%", ('green' if iErrCount == 0 else 'blue'))
  template_mod = template_mod.replace("%VARS_LIST%", strStackedRows)
  template_mod = template_mod.replace("%ERR_COUNT%", (f'{iErrCount} optimization available' if iErrCount < 2 else f'{iErrCount} optimizations available'))
  

  ## Return html
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
