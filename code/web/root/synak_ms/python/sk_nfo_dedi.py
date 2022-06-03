#!/usr/bin/python3

import re
import string

import sk__cmd
import sk__res
import sk__opn

# Array with optimizations and explanations
arrValues = {
    'fs.file-max' :                     [ '>=',   '2097152',                  'Influences the maximum number of clients connected simultaneously.' ],
    'net.core.somaxconn' :              [ '>=',   '4096',                     "Could be useful on highloaded servers where new connection rate is bursty." ],
    'net.core.rmem_max' :               [ '>=',   '16777216',                 'Could reduce bandwidth usage.' ],
    'net.core.wmem_max' :               [ '>=',   '16777216',                 'Could reduce bandwidth usage.' ],
    'net.core.rmem_default' :           [ '>=',   '16777216',                 'Could reduce bandwidth usage.<br/>Does not override the global net.core.rmem_max.' ],
    'net.core.wmem_default' :           [ '>=',   '16777216',                 'Could reduce bandwidth usage.<br/>Does not override the global net.core.rmem_max.' ],
    'net.ipv4.ip_local_port_range' :    [ '==',   '15000 61000',              'Could increase the maximum number of clients connecting.' ],
    'net.ipv4.tcp_tw_reuse' :           [ '==',   '0',                        'When enabled, presents difficulties in correctly managing multiple clients behind the same IP (NAT).' ],
    'net.ipv4.tcp_rfc1337' :            [ '==',   '0',                        'An option generally disabled which can have negative consequences.' ],
    'net.ipv4.tcp_mem' :                [ '>=',   '1638400 1638400 1638400',  'Could reduce bandwidth usage.<br/>Max(tcp_wmem) * 2 * (simultaneous clients average) / 4096<br/>This is measured in units of pages (4096 bytes).<br/>Note that TCP actually allocates twice the size of the buffer requested.<br/>Also, buffer size net.ipv4 values apply for both IPv4 and IPv6.' ],
    'net.ipv4.tcp_rmem' :               [ '>=',   '4096 87380 16777216',      'Could reduce bandwidth usage.' ],
    'net.ipv4.tcp_wmem' :               [ '>=',   '4096 87380 16777216',      'Could reduce bandwidth usage.' ],
    'net.ipv4.tcp_synack_retries' :     [ '==',   '2',                        'Could increase the dedicated server availability.' ],
    'net.ipv4.tcp_keepalive_time' :     [ '==',   '60',                       'Could increase the dedicated server availability.' ],
    'net.ipv4.tcp_keepalive_probes' :   [ '==',   '3',                        'Could increase the dedicated server availability.' ],
    'net.ipv4.tcp_keepalive_intvl' :    [ '==',   '60',                       'Could increase the dedicated server availability.' ],
    'net.ipv4.tcp_fin_timeout' :        [ '==',   '30',                       'Could increase the dedicated server availability.' ],
    'net.ipv4.tcp_congestion_control' : [ '==',   'bbr',                      "Google's TCP congestion control algorithm that resolves many both Reno and CUBIC issues (default CCAs),<br/>resulting in significant bandwidth improvements and lowering latency." ],
    'net.ipv4.tcp_syncookies' :         [ '==',   '1',                        'Should be enabled to mitigate (a little) SYN Ddos attacks.' ]
}



# Push the filled dedicated informations segment to the client
def prepare(_data):
    # Get the page template template
    template_mod = sk__opn.getTemplate("sk_nfo_dedi_tbl")

    ## Stats#1 Section
    # Get the template
    stat_raw = sk__opn.getTemplate("sk_nfo_dedi_sta")

    # Fill stats#1 with hostname
    chk, info_hst = sk__cmd.send('hostnamectl | grep -iF hostname')
    if chk is False:
        raise SystemExit
    info_hst = info_hst.split(": ")
    stat_hst = stat_raw.replace("%NAME%", info_hst[0])
    stat_hst = stat_hst.replace("%VALUE%", info_hst[1])

    # Fill stats#1 with operating system
    chk, info_lin = sk__cmd.send('hostnamectl | grep -iF operating')
    if chk is False:
        raise SystemExit
    info_lin = info_lin.split(": ")
    stat_lin = stat_raw.replace("%NAME%", info_lin[0])
    stat_lin = stat_lin.replace("%VALUE%", info_lin[1])

    # Fill stats#1 with architecture
    chk, info_arc = sk__cmd.send('hostnamectl | grep -iF architecture')
    if chk is False:
        raise SystemExit
    info_arc = info_arc.split(": ")
    stat_arc = stat_raw.replace("%NAME%", info_arc[0])
    stat_arc = stat_arc.replace("%VALUE%", info_arc[1])

    # Fill stats#1 page template with stats#1
    template_mod = template_mod.replace("%STATS_1%", stat_hst+stat_lin+stat_arc)


    ## Stats#2 Section
    # Fill stats#2 with hdd/ssd usage
    chk, info_cpu = sk__cmd.send('top -b -d1 -n1|grep -i "Cpu(s)"|head -c21|awk \'{print $2}\'')
    info_cpu = format(float(info_cpu), '.1f')
    if chk is False:
        raise SystemExit
    if float(info_cpu) < 0.1:
        info_cpu = '0.1'
    stat_cpu = stat_raw.replace("%NAME%", "CPU USAGE (%)")
    stat_cpu = stat_cpu.replace("%VALUE%", str(info_cpu))

    # Fill stats#2 with ram usage
    chk, info_ram1 = sk__cmd.send("free -m | grep -iF 'mem' | awk '{print $3}'")
    if chk is False:
        raise SystemExit
    chk, info_ram2 = sk__cmd.send("free -m | grep -iF 'mem' | awk '{print $2}'")
    if chk is False:
        raise SystemExit
    stat_ram = stat_raw.replace("%NAME%", "RAM USAGE (MB)")
    stat_ram = stat_ram.replace("%VALUE%", info_ram1 + '/' + info_ram2)

    # Fill stats#2 with hdd/ssd usage
    chk, info_hdd1 = sk__cmd.send("df --total | grep -iF total | awk '{print $3}'")
    if chk is False:
        raise SystemExit
    info_hdd1 = str(format(float(info_hdd1) / 1e+6, '.1f'))
    chk, info_hdd2 = sk__cmd.send("df --total | grep -iF total | awk '{print $2}'")
    if chk is False:
        raise SystemExit
    info_hdd2 = str(format(float() / 1e+6, '.1f'))
    stat_hdd = stat_raw.replace("%NAME%", "HDD/SSD USAGE (GB)")
    stat_hdd = stat_hdd.replace("%VALUE%", info_hdd1 + '/' + info_hdd2)

    # Fill stats#2 page template with stats#2
    template_mod = template_mod.replace("%STATS_2%", stat_cpu+stat_ram+stat_hdd)


    ## Optimizations Section
    # Get the table template
    tplRow = sk__opn.getTemplate("sk_nfo_dedi_row")
    strStackedRows = ""
    iErrCount = 0
    # Fill the table template with optimizations
    for key in arrValues:
        chk, currValue = sk__cmd.send(f'sysctl -n {key}')
        if chk is False:
            raise SystemExit
        bExpected = False
        expectedVal = arrValues[key][1]
        retrievdVal = currValue

        if arrValues[key][0] == '==':
            if len(arrValues[key][1].split()) > 1:
                bExpected = (expectedVal.split() == retrievdVal.split())
            else:
                bExpected = (retrievdVal == expectedVal)
        elif arrValues[key][0] == '>=':
            if len(arrValues[key][1].split()) > 1:
                valXpctd = arrValues[key][1].split()[-1]
                valRtrvd = retrievdVal.split()[-1]
                bExpected = (int(valRtrvd) >= int(valXpctd))
            else:
                bExpected = (int(retrievdVal) >= int(expectedVal))

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
    template_mod = template_mod.replace("%TABLE_COLOR%", ('green' if iErrCount == 0 else 'yellow'))
    template_mod = template_mod.replace("%VARS_LIST%", strStackedRows)
    template_mod = template_mod.replace("%ERR_COUNT%", (f'{iErrCount}' if iErrCount < 2 else f'{iErrCount}'))
    template_mod = template_mod.replace("%ERR_COLOR%", ('green' if iErrCount == 0 else 'yellow'))


    ## Return html
    sk__res.show("proc", template_mod)
