#!/usr/bin/python3

import json
import ipaddress
import datetime

import sk__cmd
import sk__res
import sk__dbg
import sk__sql
import sk__opn

# Push the clean UID modal to the client
def prepare(_data):
    # Get the clean UID modal template
    template_raw = sk__opn.getTemplate("sk_mod_clnu")
    # Send the modal to the client
    sk__res.show("prep", template_raw)

# Clean the sqlite database of passed dates
def process(_data):
    # Get sqlite connection
    con, conChk = sk__sql.sql_con()
    if not conChk:
        return

    # Sqlite command to calculate the number entries to delete
    strSqliteCmd = """SELECT COUNT(*) FROM t_ban;"""
    resInit, resChk = sk__sql.sql_req(con, strSqliteCmd)
    if not resChk:
        return

    # Sqlite command to delete entries
    strSqliteCmd = "DELETE FROM t_ban WHERE (julianday(c_tim) - julianday('now')) < -1"
    res, resChk = sk__sql.sql_req(con, strSqliteCmd)
    if not resChk:
        return

    # Sqlite command to check how many entries has been deleted
    strSqliteCmd = """SELECT COUNT(*) FROM t_ban;"""
    resFinal, resChk = sk__sql.sql_req(con, strSqliteCmd)
    if not resChk:
        return

    # Close sqlite
    sk__sql.sql_cls(con)

    # Push the final string to the client
    sk__dbg.message(sk__dbg.messtype.SUC, f"{resInit[0][0] - resFinal[0][0]} entries has been removed.")
