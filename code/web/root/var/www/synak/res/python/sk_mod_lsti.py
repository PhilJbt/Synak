#!/usr/bin/python3

import json
import ipaddress
import math

import sk__cmd
import sk__res
import sk__dbg
import sk__opn

# Push the filled IP banned list modal to the client
def prepare(_data):
    # Get POST data, which is the desired page number
    data = 0
    try:
        data = json.loads(_data)
    except:
        data = 0

    # Get IPv4 and IPv6 banned IPs
    strCmd = "( sudo iptables -w 5 -L INPUT -v -n | grep DROP | awk '{print $8}' & sudo ip6tables -w 5 -L INPUT -v -n | grep DROP | awk '{print $7}' )"
    strCmd += f" | head -n{(data+1)*100} | tail -n100"
    listIPv46_raw = sk__cmd.send(strCmd)

    # Get IPv4 and IPv6 banned count
    strCmd = "( sudo iptables -w 5 -L INPUT -v -n | grep DROP | awk '{print $8}' & sudo ip6tables -w 5 -L INPUT -v -n | grep DROP | awk '{print $7}' ) | wc -l"
    resCount = sk__cmd.send(strCmd)

    # Get the item template for the banned IPs list
    htmlItem = sk__opn.getTemplate("sk_mod_lsti_itm")

    # Populate place holder with the banned IPv4 and IPv6 list in the item list template
    listIPv46_mod = ''
    for itemRaw in listIPv46_raw.splitlines():
        listIPv46_mod += htmlItem.replace("%IP%", itemRaw)

    # Populate pagination template
    iPageMax = math.ceil(int(resCount) / 100)
    strPagination = """<div class="ui borderless menu">"""
    for i in range(0,iPageMax):
        strPagination += f"""<a class="item" onclick="prepareReq('sk__req', 'prep', 'sk_mod_lsti', JSON.stringify({i}));">{i+1}</a>"""
    strPagination += """</div>"""

    # Get the modal template of the banned IPs list
    template_raw = sk__opn.getTemplate("sk_mod_lsti")

    # Populate page template html with pagination
    template_mod = template_raw.replace("%PAGINATION%", strPagination)

    # If there is at least 1 banned IPv4 or IPv6
    if len(listIPv46_mod) > 0:
        # Populate the unban modal template with the IPv4 and IPv6 banned list
        template_mod = template_mod.replace("%IPV46%", listIPv46_mod)
    # Push an empty list
    else:
        template_mod = template_mod.replace("%IPV4%", 'There is no IPv4 or IPv6 IP banned.')

    # Push the unban modal template to the client
    sk__res.show("proc", template_mod)
