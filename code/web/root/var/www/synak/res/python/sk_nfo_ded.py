#!/usr/bin/python3

import re
import string

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
  # Array with optimizations and explainations
  arrValues = {
    'fs.file-max' : [ '>=', '2097152', '' ],
    'net.core.somaxconn' : [ '>=', '4096', 'Number of incoming connections.' ],
    'net.core.rmem_max' : [ '>=', '16777216', 'Maximum socket receive buffer.' ],
    'net.core.wmem_max' : [ '>=', '16777216', 'Maximum socket send buffer.' ],
    'net.core.rmem_default' : [ '>=', '16777216', 'Default socket receive buffer.' ], # Does not override the global net.core.rmem_max
    'net.core.wmem_default' : [ '>=', '16777216', 'Default socket send buffer.' ],    # Does not override the global net.core.rmem_max
    #'net.core.optmem_max' : [ '>=', '16777216', '' ],
    'net.ipv4.tcp_rfc1337' : [ '==', '0', '' ], #https://vincent.bernat.ch/fr/blog/2014-tcp-time-wait-state-linux
    'net.ipv4.tcp_rmem' : [ '>=', '4096 87380 16777216', 'Maximum total buffer-space allocatable.<br/>This is measured in units of pages (4096 bytes).\
    <br/>Note that TCP actually allocates twice the size of the buffer requested.\
    <br/>Also, IPv4 values apply for both IPv4 and IPv6.' ],
    'net.ipv4.tcp_wmem' : [ '>=', '4096 87380 16777216', 'Maximum total buffer-space allocatable.<br/>This is measured in units of pages (4096 bytes).\
    <br/>Note that TCP actually allocates twice the size of the buffer requested.\
    <br/>Also, IPv4 values apply for both IPv4 and IPv6.' ],
    'net.ipv4.tcp_mem' : [ '>=', '1638400 1638400 1638400', 'Max(tcp_wmem) * 2 * (simultaneous clients average) / 4096\
    <br/>Note that TCP actually allocates twice the size of the buffer requested.\
    <br/>Also, IPv4 values apply for both IPv4 and IPv6.' ],
    'net.ipv4.tcp_synack_retries' : [ '==', '2', 'Number of times SYNACKs for passive TCP connection.' ],
    'net.ipv4.tcp_keepalive_time' : [ '==', '60', 'Interval between the last data packet sent (simple ACKs are not considered data) and the first keepalive probe.' ],
    'net.ipv4.tcp_keepalive_probes' : [ '==', '3', 'Number of unacknowledged probes to send before considering the connection dead and notifying the application layer.' ],
    'net.ipv4.tcp_keepalive_intvl' : [ '==', '60', 'Interval between subsequential keepalive probes, regardless of what the connection has exchanged in the meantime.' ],    
    'net.ipv4.tcp_congestion_control' : [ '==', 'bbr', '' ], #https://www.techrepublic.com/article/how-to-enable-tcp-bbr-to-improve-network-speed-on-linux/
    'net.ipv4.tcp_syncookies' : [ '==', '1', '' ]
  }

  # Get the table template
  fileRow = open("../template/sk_nfo_ded_row.tpl", "r")
  tplRow = fileRow.read()
  strStackedRows = ""
  iErrCount = 0
  # Fill the table template with optimizations
  for key in arrValues:
    currValue = sk__cmd.send(f'sysctl -n {key}')
    bExpected = False
    expectedVal = ""
    retrievdVal = ""
    if not currValue.isdigit():
      expectedVal = arrValues[key][1].split()[-1]
      retrievdVal = currValue.split()[-1]
    else:
      expectedVal = arrValues[key][1]
      retrievdVal = currValue
    if re.search('[a-zA-Z]', currValue):
      bExpected = (retrievdVal == expectedVal)
    else:
      strCondition = retrievdVal + arrValues[key][0] + expectedVal
      bExpected = eval(strCondition)
    if bExpected is False:
      iErrCount += 1
    tplRowTemp = tplRow.replace("%NAME%", key)
    tplRowTemp = tplRowTemp.replace("%VALDEF%", arrValues[key][1])
    tplRowTemp = tplRowTemp.replace("%VALCUR%", currValue)
    tplRowTemp = tplRowTemp.replace("%ICON%", ('green checkmark' if bExpected else 'yellow exclamation'))
    tplRowTemp = tplRowTemp.replace("%STATUS%", arrValues[key][2])
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
