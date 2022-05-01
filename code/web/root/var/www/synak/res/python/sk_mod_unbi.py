#!/usr/bin/python3

import json
import ipaddress

import sk__cmd
import sk__res
import sk__dbg

# Push modal disclaimer about killing MS process
def prepare(_data):
  # Get IPv4 and IPv6 banned IPs
  listIPv4_raw = sk__cmd.send("sudo iptables -L INPUT -v -n | grep DROP | awk '{print $8}'")
  listIPv6_raw = sk__cmd.send("sudo ip6tables -L INPUT -v -n | grep DROP | awk '{print $7}'")

  # Get the item list template
  fileItem = open("../template/sk_mod_unbi_itm.tpl", "r")
  htmlItem = fileItem.read()

  # Replace the banned IPv4 list to the item list template
  listIPv4_mod = ""
  for itemRaw in listIPv4_raw.splitlines():
    listIPv4_mod += htmlItem.replace("%IP%", itemRaw)

  # Replace the banned IPv6 list to the item list template
  listIPv6_mod = ""
  for itemRaw in listIPv6_raw.splitlines():
    listIPv6_mod += htmlItem.replace("%IP%", itemRaw)

  # Get the unban modal template
  file = open("../template/sk_mod_unbi.tpl", "r")
  template_raw = file.read()
  # If there is at least 1 banned IPv4
  if len(listIPv4_mod) > 0:
    # Push the IPv4 banned list to the unban modal template
    template_mod = template_raw.replace("%IPV4%", listIPv4_mod)
  # Push an empty list
  else:
    template_mod = template_raw.replace("%IPV4%", 'There are no banned IPv4 IPs.')
  # If there is at least 1 banned IPv6
  if len(listIPv6_mod) > 0:
    # Push the IPv6 banned list to the unban modal template
    template_mod = template_mod.replace("%IPV6%", listIPv6_mod)
  # Push an empty list
  else:
    template_mod = template_mod.replace("%IPV6%", 'There are no banned IPv6 IPs.')

  # Push the unban modal template to the client
  sk__res.show("prep", template_mod)

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
