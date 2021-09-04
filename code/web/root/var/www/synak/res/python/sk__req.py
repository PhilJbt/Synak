#!/usr/bin/python3

import sys
import select
import json
import os.path

import sk__dbg
import sk_mng_srt
import sk_mng_stp
import sk_mng_kll
import sk_mod_ban
import sk_mod_unb
import sk_log_get
import sk_log_era
#import sk_stt_sms
import sk_stt_ded

# Get POST data and parse the Json
try:
  jsonPost = json.load(sys.stdin)
except:
  sk__dbg.message(sk__dbg.messtype.ATT, "Request undefined.")
else:
  file_dict = {
    'sk_mng_srt' : sk_mng_srt,
    'sk_mng_stp' : sk_mng_stp,
    'sk_mng_kll' : sk_mng_kll,
    'sk_mod_ban' : sk_mod_ban,
    'sk_mod_unb' : sk_mod_unb,    
    'sk_log_get' : sk_log_get,
    'sk_log_era' : sk_log_era,
    #'sk_stt_sms' : sk_stt_sms,
    'sk_stt_ded' : sk_stt_ded,
  }

  # Check all args are in the POST data
  if ("file" not in jsonPost or "type" not in jsonPost
    or "data" not in jsonPost or "auth" not in jsonPost):
    sk__dbg.message(sk__dbg.messtype.ERR, "An argument is missing in the request.")
  else:
    # Get the script filename
    file_name = jsonPost["file"]
    # If key auth permissions are enabled
    if os.path.isfile("../webpanel.permissions"):
      # Get the modal stop template
      filePerms = open("../webpanel.permissions", "r")
      infoPerms = filePerms.read()
      # Key auth file is a valid json
      try:
        jsonPerms = json.loads(infoPerms)
      # Json is not valid, stop the script and push an error message to the client
      except Exception as e:
        sk__dbg.message(sk__dbg.messtype.ERR, f"The permissions file (synak/res/webpanel.permissions) is not valid: {str(e)}")  
      # Push an error message to the client if the user does not have permissions to execute this script, else continue the script
      else:
        if (jsonPost["auth"] not in jsonPerms
          or file_name not in jsonPerms[jsonPost["auth"]]):
          sk__dbg.message(sk__dbg.messtype.KEY, "You do not have the necessary permissions to access this feature.")
          exit()

    # Script doesn't exist
    if file_name not in file_dict:
      sk__dbg.message(sk__dbg.messtype.ATT, "script filename does not exist")
    # Exec the Prepare() function 
    elif jsonPost["type"] == "prep":
      file_dict[file_name].prepare(jsonPost['data'])
    # Exec the Process() function 
    elif jsonPost["type"] == "proc":
      file_dict[file_name].process(jsonPost['data'])
    # Filename exists, but not the provided type
    else:
      sk__dbg.message(sk__dbg.messtype.ATT, "type request undefined")
