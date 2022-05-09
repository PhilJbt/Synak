#!/usr/bin/python3

import json
import ipaddress

import sk__cmd
import sk__res
import sk__dbg
import sk__sql

# Push the filled UID banned list modal to the client
def prepare(_data):
  # Get sqlite connection
  con, conChk = sk__sql.sql_con()
  if not conChk:
    return

  # Get banned UIDs
  res, resChk = sk__sql.sql_req(con, "SELECT c_uid FROM t_ban")
  if not resChk:
    return

  # Close sqlite
  sk__sql.sql_cls(con)

  # Get the item list template
  fileItem = open("../template/sk_mod_lstu_itm.tpl", "r")
  htmlItem = fileItem.read()

  # Replace the banned UIDs list to the item list template
  listUid_mod = ""
  for row in res:
    listUid_mod += htmlItem.replace("%UID%", row[0])

  # Get the UID banned list modal template
  file = open("../template/sk_mod_lstu.tpl", "r")
  template_raw = file.read()
  # If there is at least 1 banned UID
  if len(listUid_mod) > 0:
    # Populate the list modal template with the banned UIDs
    template_mod = template_raw.replace("%UIDS%", listUid_mod)
  # Push an empty list
  else:
    template_mod = template_raw.replace("%UIDS%", 'There are no banned UIDs.')

  # Push the unban modal template to the client
  sk__res.show("proc", template_mod)
