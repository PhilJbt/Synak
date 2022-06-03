#!/usr/bin/python3

import select
import json
import os.path
import base64
import sys
sys.path.insert(1, '/synak_ms/python')

import sk__dbg
import sk_mng_strt
import sk_mng_stop
import sk_mng_kill
import sk_mng_optn
import sk_mng_chck
import sk_mod_bani
import sk_mod_unbi
import sk_mod_lsti
import sk_mod_banu
import sk_mod_unbu
import sk_mod_lstu
import sk_mod_clnu
import sk_log_rtrv
import sk_log_eras
import sk_nfo_cnfg
import sk_nfo_syms
import sk_nfo_dedi

# Get POST data and parse the Json request
try:
    jsonPost = json.load(sys.stdin)
except:
    sk__dbg.message(sk__dbg.messtype.ATT, "Request undefined.")
else:
    file_dict = {
        'sk_mng_strt' : sk_mng_strt,
        'sk_mng_stop' : sk_mng_stop,
        'sk_mng_kill' : sk_mng_kill,
        'sk_mng_optn' : sk_mng_optn,
        'sk_mng_chck' : sk_mng_chck,
        'sk_mod_bani' : sk_mod_bani,
        'sk_mod_unbi' : sk_mod_unbi,
        'sk_mod_lsti' : sk_mod_lsti,
        'sk_mod_banu' : sk_mod_banu,
        'sk_mod_unbu' : sk_mod_unbu,
        'sk_mod_lstu' : sk_mod_lstu,
        'sk_mod_clnu' : sk_mod_clnu,
        'sk_log_rtrv' : sk_log_rtrv,
        'sk_log_eras' : sk_log_eras,
        'sk_nfo_cnfg' : sk_nfo_cnfg,
        'sk_nfo_syms' : sk_nfo_syms,
        'sk_nfo_dedi' : sk_nfo_dedi,
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
                authKey = base64.b64decode(jsonPost["auth"]).decode('utf-8')
                if (authKey not in jsonPerms
                    or file_name not in jsonPerms[authKey]):
                    sk__dbg.message(sk__dbg.messtype.KEY, f"You do not have the necessary permissions to access this feature ({file_name}).")
                    exit()

        # Script doesn't exist
        if file_name not in file_dict:
            sk__dbg.message(sk__dbg.messtype.ATT, f"script filename does not exist ({file_name})")
        # Exec the Prepare() function
        elif jsonPost["type"] == "prep":
            file_dict[file_name].prepare(jsonPost['data'])
        # Exec the Process() function
        elif jsonPost["type"] == "proc":
            file_dict[file_name].process(jsonPost['data'])
        # Filename exists, but not the provided type
        else:
            sk__dbg.message(sk__dbg.messtype.ATT, "type request undefined")
