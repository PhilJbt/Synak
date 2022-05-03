#!/usr/bin/python3

import sqlite3
import json
import ipaddress

import sk__cmd
import sk__res
import sk__dbg

# Push modal disclaimer about unban UID process
def prepare(_data):
  # Open database
  dbPath = r'../db/blacklist_uid.db'
  con = None
  try:
    con = sqlite3.connect(dbPath)
  except sqlite3.OperationalError:
    sk__dbg.message(sk__dbg.messtype.ERR, "Can't connect to /var/www/synak/res/db/blacklist_uid.db.")
    return

  # Get banned UIDs
  res = None
  try:
    cur = con.cursor()
    res = cur.execute("SELECT c_uid FROM t_ban")
    res = cur.fetchall()
  except sqlite3.Error as er:
    sk__dbg.message(sk__dbg.messtype.ERR, 'Error when UIDs retrieval: %s' % (' '.join(er.args)))
    return

  # Get the item list template
  fileItem = open("../template/sk_mod_unbu_itm.tpl", "r")
  htmlItem = fileItem.read()

  # Replace the banned UIDs list to the item list template
  listUid_mod = ""
  for row in res:
    listUid_mod += htmlItem.replace("%UID%", row[0])

  # Get the unban modal template
  file = open("../template/sk_mod_unbu.tpl", "r")
  template_raw = file.read()
  # If there is at least 1 banned UID
  if len(listUid_mod) > 0:
    # Push the UIDs banned list to the unban modal template
    template_mod = template_raw.replace("%UIDS%", listUid_mod)
  # Push an empty list
  else:
    template_mod = template_raw.replace("%UIDS%", 'There are no banned UIDs.')

  # Push the unban modal template to the client
  sk__res.show("prep", template_mod)

# Push segment to client
def process(_data):
  # Declare the start of the html content division holding the list of unbanned UIDs
  strListUids = '<div class="header">Successfully unbanned IP</div><div class="ui bulleted list">'

  # Sqlite command to unban UIDs
  strSqliteCmd = "DELETE FROM t_ban WHERE c_uid IN ("

  # Get POST data
  data = json.loads(_data)
  # For all UIDs in the POST data
  for i, elem in enumerate(data):
    # Add the unbanned UID to the list of unvanned UIDs
    strListUids += f'<div class="item">{elem}</div>'
    # Add the unbanned UID to the sqlite command
    strSqliteCmd += f"'{elem}'"
    if i < len(data) - 1:
      strSqliteCmd += ", "
    else:
      strSqliteCmd += ");"

  # Close the html content division
  strListUids += '</div>'

  # Open database
  dbPath = r'../db/blacklist_uid.db'
  con = None
  try:
    con = sqlite3.connect(dbPath)
  except sqlite3.OperationalError:
    sk__dbg.message(sk__dbg.messtype.ERR, "Can't connect to /var/www/synak/res/db/blacklist_uid.db.")
    return

  # Erase UID from sqlite database
  cur = con.cursor()
  cur.execute(strSqliteCmd)
  con.commit()

  # Close sqlite connection
  if con :
    con.close()

  # Push the segment template to the client
  sk__dbg.message(sk__dbg.messtype.SUC, strListUids)
