#!/usr/bin/python3

import json
import ipaddress

import sk__cmd
import sk__res
import sk__dbg

def prepare(_data):  
  file = open("../template/sk_mod_ban.tpl", "r")
  template_raw = file.read()
  template_mod = template_raw.replace("%VAR_1%", "test")
  sk__res.show("prep", template_mod)

def process(_data):
  data = json.loads(_data)

  strIpVld = '<div class="header">Successfully banned IP</div><div class="ui bulleted list">'
  strIpErr = '<div class="header">Not valid IP</div><div class="ui bulleted list">'
  ipVldNbr = 0
  ipErrNbr = 0

  for elem in data:
    try:
      ip = ipaddress.ip_address(elem)
      if ip.version == 4:
        sk__cmd.send(f'sudo iptables -A INPUT -s {elem} -j DROP')
      elif ip.version == 6:
        sk__cmd.send(f'sudo ip6tables -A INPUT -s {elem} -j DROP')
      strIpVld += f'<div class="item">{elem}</div>'
      ipVldNbr += 1
    except:
      strIpErr += f'<div class="item">{elem}</div>'
      ipErrNbr += 1
  strIpVld += '</div>'
  strIpErr += '</div>'

  messType = None
  if (ipVldNbr > 0) and (ipErrNbr == 0):
    messType = sk__dbg.messtype.SUC
  elif (ipVldNbr == 0) and (ipErrNbr > 0):
    messType = sk__dbg.messtype.ERR
  else:
    messType = sk__dbg.messtype.ATT

  sendline = ""
  if ipVldNbr > 0:
    sendline += strIpVld
  if ipErrNbr > 0:
    sendline += strIpErr
  
  sk__dbg.message(messType, sendline)
