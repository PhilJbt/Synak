#!/usr/bin/python3

import sqlite3
import json
import ipaddress

import sk__cmd
import sk__res
import sk__dbg

# Push modal disclaimer about killing MS process
def prepare(_data):
  # Get the ban modal template
  file = open("../template/sk_mod_banu.tpl", "r")
  template_raw = file.read()
  # Send the modal to the client
  sk__res.show("prep", template_raw)

# Push segment to client
def process(_data):
  # Open or create database
  dbPath = r'../db/blacklist_uid.db'
  con = None
  try:
    con = sqlite3.connect(dbPath)
  except sqlite3.OperationalError:
    sk__dbg.message(sk__dbg.messtype.ERR, "Can't connect to /var/www/synak/res/db/blacklist_uid.db.")
    return

  # If table does not exist, create table
  cur = con.cursor()
  cur.execute("""SELECT count(name) FROM sqlite_master WHERE type='table' AND name='t_ban'""")
  if cur.fetchone()[0] == 0 :
    try:
      cur.execute("""CREATE TABLE if not exists t_ban(c_uid CHAR(32) NOT NULL PRIMARY KEY)""")
      con.commit()
    except sqlite3.Error as er:
      sk__dbg.message(sk__dbg.messtype.ERR, 'Error when creating table t_ban: %s' % (' '.join(er.args)))
      return

  # Get POST data
  data = json.loads(_data)

  # Insert every UID in the SQL database
  for elem in data:
    try:
      cur.execute(f'INSERT OR REPLACE INTO "t_ban" ("c_uid") values("{elem}");')
      con.commit()
    except sqlite3.Error as er:
      sk__dbg.message(sk__dbg.messtype.ERR, 'Error when inserting UID: %s' % (' '.join(er.args)))
      return

  # Close sqlite connection
  if con :
    con.close()

  # For every IP in the POST data
  strResult = '<div class="header">Successfully banned UIDs</div><div class="ui bulleted list">'
  for elem in data:
    strResult += f'<div class="item">{elem}</div>'

  # Close the html content division
  strResult += '</div>'

  # Push the final string to the client
  sk__dbg.message(sk__dbg.messtype.SUC, strResult)
