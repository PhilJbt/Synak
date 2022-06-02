#!/usr/bin/python3

import json
import ipaddress

import sk__cmd
import sk__res
import sk__dbg
import sk__opn

# Push the IP unban modal to the client
def prepare(_data):
    # Get the ban modal template
    template_raw = sk__opn.getTemplate("sk_mod_unbi")
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
        bValid = True
        try:
            ip = ipaddress.ip_address(elem)
        # An error occured while casting str to ip_addr, do nothing (== do not add this IP to the list)
        except:
            bValid = False
            pass

        if bValid:
            # If IPv4, unban with iptables
            if ip.version == 4:
                chk, res = sk__cmd.send(f'sudo iptables -w 60 -D INPUT -s {elem} -j DROP')
                if chk is False:
                    raise SystemExit
            # If IPv4, unban with ip6tables
            elif ip.version == 6:
                chk, res = sk__cmd.send(f'sudo ip6tables -w 60 -D INPUT -s {elem} -j DROP')
                if chk is False:
                    raise SystemExit
            # Add the unbanned IP to the list of unvanned IPs
            strIpVld += f'<div class="item">{elem}</div>'

    # Close the html content division
    strIpVld += '</div>'

    # Push the segment template to the client
    sk__dbg.message(sk__dbg.messtype.SUC, strIpVld)
