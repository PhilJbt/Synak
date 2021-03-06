#!/usr/bin/python3

import json
import ipaddress

import sk__cmd
import sk__res
import sk__dbg
import sk__sql
import sk__opn

# Push the UID unban modal to the client
def prepare(_data):
    # Get the ban modal template
    template_raw = sk__opn.getTemplate("sk_mod_unbu")
    # Send the modal to the client
    sk__res.show("prep", template_raw)

# Push segment to client
def process(_data):
    # Get sqlite connection
    con, conChk = sk__sql.sql_con()
    if not conChk:
        return

    # Get POST data
    data = json.loads(_data)

    # For every IP in the POST data
    strResult = '<div class="header">Successfully unbanned UIDs</div><div class="ui bulleted list">'

    # Sqlite command to unban UIDs
    strSqliteCmd = "DELETE FROM t_ban WHERE c_uid IN ("

    # Get POST data
    data = json.loads(_data)

    # For all UIDs in the POST data
    for i, elem in enumerate(data):
        # Add the unbanned UID to the sqlite command
        strSqliteCmd += f"'{elem}'"
        # Populate the HTML segment with the unbanned UID
        strResult += f'<div class="item">{elem}</div>'
        if i < len(data) - 1:
            strSqliteCmd += ", "
        else:
            # Close the sqlite request
            strSqliteCmd += ");"
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
