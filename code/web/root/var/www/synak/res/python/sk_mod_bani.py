#!/usr/bin/python3

import json
import ipaddress

import sk__cmd
import sk__res
import sk__dbg
import sk__opn

# Push the UID banning modal to the client
def prepare(_data):
    # Get the ban modal template
    template_raw = sk__opn.getTemplate("sk_mod_bani")
    # Send the modal to the client
    sk__res.show("prep", template_raw)

# Push segment to client
def process(_data):
    # Declare feedback vars
    strIpVld = '<div class="header">Successfully banned IP</div><div class="ui bulleted list">'
    strIpErr = '<div class="header">Not valid IP</div><div class="ui bulleted list">'
    # Declare success/error IP ban number vars
    ipVldNbr = 0
    ipErrNbr = 0

    # Get POST data
    data = json.loads(_data)

    # For every IP in the POST data
    for elem in data:
        elem = elem.replace(' ', '')
        if len(elem) > 0:
            # Try to cast str to ip_addr
            try:
                ip = ipaddress.ip_address(elem)
                # IPv4 detected, ban it with iptables
                if ip.version == 4:
                    sk__cmd.send(f'sudo iptables -w 60 -A INPUT -s {elem} -j DROP')
                # IPv6 detected, ban it with ip6tables
                elif ip.version == 6:
                    sk__cmd.send(f'sudo ip6tables -w 60 -A INPUT -s {elem} -j DROP')
                # Add the banned IP to the corresponding feedback stack
                strIpVld += f'<div class="item">{elem}</div>'
                # Increment the number of banned IP by one
                ipVldNbr += 1
            # Can't cast str to ip_addr
            except:
                # Add the invalid IP to the corresponding feedback stack
                strIpErr += f'<div class="item">{elem}</div>'
                # Increment the number of invalid IP by one
                ipErrNbr += 1

    # Close the html content division
    strIpVld += '</div>'
    strIpErr += '</div>'

    # Declare the message type to push to the client
    messType = None
    # There is no invalid IP, choose the success type
    if (ipVldNbr > 0) and (ipErrNbr == 0):
        messType = sk__dbg.messtype.SUC
    # There is no valid IP, choose the error type
    elif (ipVldNbr == 0) and (ipErrNbr > 0):
        messType = sk__dbg.messtype.ERR
    # There is both valid and invalid IP, choose the warning type
    else:
        messType = sk__dbg.messtype.ATT

    # Declare the final string containing the list of valid and invalid IP addresses to push to the client
    sendline = ""
    # There is at least one valid IP, push the corresponding list to the final string
    if ipVldNbr > 0:
        sendline += strIpVld
    # There is at least one invalid IP, push the corresponding list to the final string
    if ipErrNbr > 0:
        sendline += strIpErr

    # Push the final string to the client
    sk__dbg.message(messType, sendline)
