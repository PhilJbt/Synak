#!/usr/bin/python3

import json
import ipaddress

import sk__cmd
import sk__res
import sk__dbg

# Push the IP unban modal to the client
def prepare(_data):
  # Get the ban modal template
  file = open("../template/sk_mod_unbi.tpl", "r")
  template_raw = file.read()
  # Send the modal to the client
  sk__res.show("prep", template_raw)

# Push segment to client
def process(_data):
  # Declare the start of the html content division holding the list of unbanned IPs
  strIpVld = '<div class="header">Successfully unbanned IP</div><div class="ui bulleted list">'

  # Get POST data
  data = json.loads(_data)
  # For all IPs in the POST data
  for elem in data:
    # Try to cast str to ip_addr
    try:
      ip = ipaddress.ip_address(elem)
      # If IPv4, unban with iptables
      if ip.version == 4:
        sk__cmd.send(f'sudo iptables -D INPUT -s {elem} -j DROP')
      # If IPv4, unban with ip6tables
      elif ip.version == 6:
        sk__cmd.send(f'sudo ip6tables -D INPUT -s {elem} -j DROP')
      # Add the unbanned IP to the list of unvanned IPs
      strIpVld += f'<div class="item">{elem}</div>'
    # An error occured while casting str to ip_addr, do nothing (== do not add this IP to the list)
    except:
      pass

  # Close the html content division
  strIpVld += '</div>'

  # Push the segment template to the client
  sk__dbg.message(sk__dbg.messtype.SUC, strIpVld)