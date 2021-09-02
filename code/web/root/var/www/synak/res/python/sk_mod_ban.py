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
  for elem in data:
    try:
      ip = ipaddress.ip_address(elem)
      if ip.version == 4:
        sk__cmd.send(f'sudo iptables -A INPUT -s {elem} -j DROP')
      elif ip.version == 6:
        sk__cmd.send(f'sudo ip6tables -A INPUT -s {elem} -j DROP')
    except:
      sk__dbg.message(sk__dbg.messtype.ERR, f'An error occured when processing the "{elem}" IP.')
    else:
      sk__dbg.message(sk__dbg.messtype.SUC, f'Banned IP: "{data}"')
