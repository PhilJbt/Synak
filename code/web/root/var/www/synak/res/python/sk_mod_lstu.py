#!/usr/bin/python3

import json
import ipaddress
import datetime
import math

import sk__cmd
import sk__res
import sk__dbg
import sk__sql
import sk__opn

# Push the filled UID banned list modal to the client
def prepare(_data):
    # Get sqlite connection
    con, conChk = sk__sql.sql_con()
    if not conChk:
        return

    # Get POST data
    data = 0
    try:
        data = json.loads(_data)
    except:
        data = 0

    # Get banned UIDs
    resUIDs, resChk = sk__sql.sql_req(con, f"SELECT c_uid, c_tim FROM t_ban limit 100 offset {data}")
    if not resChk:
        return

    # Get UIDs count
    resCount, resChk = sk__sql.sql_req(con, f"SELECT COUNT(*) c_uid FROM t_ban")
    if not resChk:
        return

    # Close sqlite
    sk__sql.sql_cls(con)

    # Populate pagination template
    iPageMax = math.ceil(resCount[0][0] / 100)
    strPagination = """<div class="ui borderless menu">"""
    for i in range(0,iPageMax):
        strPagination += f"""<a class="item" onclick="prepareReq('sk__req', 'prep', 'sk_mod_lstu', JSON.stringify({i*100}));">{i+1}</a>"""
    strPagination += """</div>"""

    # Get the item list template
    htmlItem = sk__opn.getTemplate("sk_mod_lstu_itm")

    # Get the current date
    dateNowTP = datetime.datetime.today()

    # Replace the banned UIDs list to the item list template
    listUid_mod = ""
    for row in resUIDs:
        dateEndBan = 'NULL'
        dateEndBan = 'NULL'
        diffDate = 0
        try:
            dateEndBan = datetime.datetime.strptime(row[1], "%Y-%m-%d")
            diffDate = (dateEndBan - dateNowTP).days + 2 # Same date returns -1
        except:
            pass
        htmlItem_mod = htmlItem.replace("%UID%", row[0])
        htmlItem_mod = htmlItem_mod.replace("%DAYLEFT%", '0' if diffDate < 0 else str(diffDate))
        htmlItem_mod = htmlItem_mod.replace("%DATESTR%", row[1])
        listUid_mod += htmlItem_mod.replace("%COLOR%", 'red' if diffDate > 0 else 'green')

    # Get the UID banned list modal template
    template_raw = sk__opn.getTemplate("sk_mod_lstu")

    # Populate page template html with pagination
    template_mod = template_raw.replace("%PAGINATION%", strPagination)

    # If there is at least 1 banned UID
    if len(listUid_mod) > 0:
        # Populate the list modal template with the banned UIDs
        template_mod = template_mod.replace("%UIDS%", listUid_mod)
    # Push an empty list
    else:
        template_mod = template_mod.replace("%UIDS%", 'There are no banned UIDs.')

    # Push the unban modal template to the client
    sk__res.show("proc", template_mod)
