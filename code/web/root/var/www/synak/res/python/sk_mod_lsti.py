#!/usr/bin/python3

import json
import ipaddress

import sk__cmd
import sk__res
import sk__dbg
import sk__opn

# Push the filled IP banned list modal to the client
def prepare(_data):
    # Get IPv4 and IPv6 banned IPs
    listIPv4_raw = sk__cmd.send("sudo iptables -L INPUT -v -n | grep DROP | awk '{print $8}'")
    listIPv6_raw = sk__cmd.send("sudo ip6tables -L INPUT -v -n | grep DROP | awk '{print $7}'")

    # Get the item template for the banned IPs list
    htmlItem = sk__opn.getTemplate("sk_mod_lsti_itm")

    # Populate place holder with the banned IPv4 list in the item list template
    listIPv4_mod = ""
    for itemRaw in listIPv4_raw.splitlines():
        listIPv4_mod += htmlItem.replace("%IP%", itemRaw)

    # Populate place holder with the banned IPv6 list in the item list template
    listIPv6_mod = ""
    for itemRaw in listIPv6_raw.splitlines():
        listIPv6_mod += htmlItem.replace("%IP%", itemRaw)

    # Get the modal template of the banned IPs list
    template_raw = sk__opn.getTemplate("sk_mod_lsti")
    # If there is at least 1 banned IPv4
    if len(listIPv4_mod) > 0:
        # Populate the unban modal template with the IPv4 banned list
        template_mod = template_raw.replace("%IPV4%", listIPv4_mod)
    # Push an empty list
    else:
        template_mod = template_raw.replace("%IPV4%", 'There are no banned IPv4 IPs.')
    # If there is at least 1 banned IPv6
    if len(listIPv6_mod) > 0:
        # Populate the unban modal template with the IPv6 banned list
        template_mod = template_mod.replace("%IPV6%", listIPv6_mod)
    # Push an empty list
    else:
        template_mod = template_mod.replace("%IPV6%", 'There are no banned IPv6 IPs.')

    # Push the unban modal template to the client
    sk__res.show("proc", template_mod)
