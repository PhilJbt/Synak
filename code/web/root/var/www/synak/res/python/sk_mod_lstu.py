#!/usr/bin/python3

import json
import ipaddress
import datetime

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

    # Get banned UIDs
    res, resChk = sk__sql.sql_req(con, "SELECT c_uid, c_tim FROM t_ban")
    if not resChk:
        return

    # Close sqlite
    sk__sql.sql_cls(con)

    # Get the item list template
    htmlItem = sk__opn.getTemplate("sk_mod_lstu_itm")

    # Get the current date
    dateNowTP = datetime.datetime.today()

    # Replace the banned UIDs list to the item list template
    listUid_mod = ""
    for row in res:
        dateEndBan = datetime.datetime.strptime(row[1], "%Y-%m-%d")
        diffDate = (dateEndBan - dateNowTP).days + 2 # Same date returns -1
        htmlItem_mod = htmlItem.replace("%UID%", row[0])
        htmlItem_mod = htmlItem_mod.replace("%DAYLEFT%", '0' if diffDate < 0 else str(diffDate))
        htmlItem_mod = htmlItem_mod.replace("%DATESTR%", row[1])
        listUid_mod += htmlItem_mod.replace("%COLOR%", 'red' if diffDate > 0 else 'green')

    # Get the UID banned list modal template
    template_raw = sk__opn.getTemplate("sk_mod_lstu")
    # If there is at least 1 banned UID
    if len(listUid_mod) > 0:
        # Populate the list modal template with the banned UIDs
        template_mod = template_raw.replace("%UIDS%", listUid_mod)
    # Push an empty list
    else:
        template_mod = template_raw.replace("%UIDS%", 'There are no banned UIDs.')

    # Push the unban modal template to the client
    sk__res.show("proc", template_mod)
