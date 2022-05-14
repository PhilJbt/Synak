#!/usr/bin/python3

import json
import ipaddress
import datetime

import sk__cmd
import sk__res
import sk__dbg
import sk__sql
import sk__opn

# Push the UID banning modal to the client
def prepare(_data):
    # Get the ban modal template
    template_raw = sk__opn.getTemplate("sk_mod_banu")
    # Get the ban modal template
    template_itm = sk__opn.getTemplate("sk_mod_banu_itm")
    # Populate the first pre-filled node in the modal and the HTML in the javascript code for add a new node
    template_mod = template_raw.replace("%BAN_ITEM%", template_itm)
    # Send the modal to the client
    sk__res.show("prep", template_mod)

# Push segment to client
def process(_data):
    # Get sqlite connection
    con, conChk = sk__sql.sql_con()
    if not conChk:
        return

    # Get POST data
    data = json.loads(_data)

    # For every IP in the POST data
    strResult = '<div class="header">Successfully banned UIDs</div><div class="ui bulleted list">'

    # Get today date
    dateTodayTP = datetime.date.today()

    # Sqlite command to unban UIDs
    strSqliteCmd = "INSERT OR REPLACE INTO 't_ban' ('c_uid', 'c_tim') VALUES "

    # Get POST data
    data = json.loads(_data)

    # For all UIDs in the POST data
    for i, elem in enumerate(data):
        # Translate days of ban into date
        try:
            banDaysInt = int(elem[1])
        except:
            sk__dbg.message(sk__dbg.messtype.ERR, f"This value is not an number: {elem[1]}")
        banDaysDate = dateTodayTP + datetime.timedelta(days=banDaysInt)

        # Add the banned UID to the sqlite command
        strSqliteCmd += f"('{elem[0]}', '{banDaysDate}')"

        # Populate the HTML segment with the banned UID
        strResult += f'<div class="item">{elem[0]} banned until {banDaysDate} included</div>'
        if i < len(data) - 1:
            strSqliteCmd += ", "
        else:
            # Close the sqlite request
            strSqliteCmd += ";"
            # Close the HTML segment
            strResult += '</div>'

    # Execute sqlite request
    res, resChk = sk__sql.sql_req(con, strSqliteCmd)
    if not resChk:
        return

    # Close sqlite
    sk__sql.sql_cls(con)

    # Push the final string to the client
    sk__dbg.message(sk__dbg.messtype.SUC, strResult)
