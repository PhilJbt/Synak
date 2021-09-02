#!/usr/bin/python3

import json
import ipaddress

import sk__cmd
import sk__res
import sk__dbg

def prepare(_data): 
  listIPv4_raw = sk__cmd.send("sudo iptables -L INPUT -v -n | grep DROP | awk '{print $8}'")
  listIPv6_raw = sk__cmd.send("sudo ip6tables -L INPUT -v -n | grep DROP | awk '{print $7}'")

  htmlItem = '<div class="item">\
    <div class="left floated content">\
      <div class="inline field">\
        <div class="ui toggle checkbox">\
          <input data-ip="%IP%" type="checkbox" tabindex="0" class="hidden">\
          <label>%IP%</label>\
        </div>\
      </div>\
    </div>\
  </div>'

  listIPv4_mod = ""
  for itemRaw in listIPv4_raw.splitlines():
    listIPv4_mod += htmlItem.replace("%IP%", itemRaw)
  
  listIPv6_mod = ""
  for itemRaw in listIPv6_raw.splitlines():
    listIPv6_mod += htmlItem.replace("%IP%", itemRaw)

  file = open("../template/sk_mod_unb.tpl", "r")
  template_raw = file.read()
  if len(listIPv4_mod) > 0:
    template_mod = template_raw.replace("%IPV4%", listIPv4_mod)
  else:
    template_mod = template_raw.replace("%IPV4%", 'There are no banned IPv4 IPs.')
  if len(listIPv6_mod) > 0:
    template_mod = template_mod.replace("%IPV6%", listIPv6_mod)
  else:
    template_mod = template_mod.replace("%IPV6%", 'There are no banned IPv6 IPs.')
  sk__res.show("prep", template_mod)

def process(_data):
  #res, err = sk__skt.send()
  #if not err:
  #  sk__res.show("proc", res)
  strIpVld = '<div class="header">Successfully unbanned IP</div><div class="ui bulleted list">'
  data = json.loads(_data)
  for elem in data:
    try:
      ip = ipaddress.ip_address(elem)
      if ip.version == 4:
        sk__cmd.send(f'sudo iptables -D INPUT -s {elem} -j DROP')
      elif ip.version == 6:
        sk__cmd.send(f'sudo ip6tables -D INPUT -s {elem} -j DROP')
      strIpVld += f'<div class="item">{elem}</div>'
    except:
      pass
  strIpVld += '</div>'
  sk__dbg.message(sk__dbg.messtype.SUC, strIpVld)