#!/usr/bin/python3

import select
import json
import os
import html
import base64
from hashlib import sha256
import sys
sys.path.insert(1, '/synak_ms/wp_res/python')

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


# Entry point answering to ajax Web Panel
def sk__req():
    # Get POST data and parse the Json request
    try:
        jsonPost = json.load(sys.stdin)
    except:
        sk__dbg.message(sk__dbg.messtype.ATT, "No POST data provided.")
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

        # Get the credential cookie
        arrCookie = os.environ.get('HTTP_COOKIE').split(';')
        # Cookie is an empty string
        if len(arrCookie) == 0:
            sk__dbg.message(sk__dbg.messtype.ERR, 'Credential cookie is empty.')
            return
        # Cookie is populated with arguments
        else:
            # Declare and initialize the login/password dictionnary
            dicCredentials = {}
            # For each argument in the cookie string
            for elem in arrCookie:
                # If the element is parsable
                if elem.find('=') != -1:
                    try:
                        # Split the cookie in half
                        arrTempSplit = elem.split('=')
                    except:
                        pass
                    else:
                        # If there are two parts
                        if len(arrTempSplit) == 2:
                            # Insert 'value' (i.e. 'sk_log', 'sk_pwd') to 'key' (i.e. 'myLogin', 'myPASSW0RD')
                            dicCredentials[arrTempSplit[0].strip()] = arrTempSplit[1].strip()
            # Login or password argument does not exist
            if "sk_log" not in dicCredentials or "sk_pwd" not in dicCredentials:
                sk__dbg.message(sk__dbg.messtype.ERR, 'Credential cookie is not valid.')
                return
            # Cookie is populated with 'sk_log' and 'sk_pwd'
            else:
                # Check all args are in the POST data
                if ("file" not in jsonPost or "type" not in jsonPost or "data" not in jsonPost):
                    sk__dbg.message(sk__dbg.messtype.ERR, "An argument is missing in the request.")
                else:
                    # Get the script filename
                    file_name = jsonPost["file"]
                    # If auth permissions are enabled
                    if os.path.isfile("/synak_ms/wp_res/webpanel.permissions") == False:
                        sk__dbg.message(sk__dbg.messtype.ATT, "/synak_ms/wp_res/webpanel.permissions does not exist.")
                    else:
                        # Auth file is a valid json
                        try:
                            # Open the permission file
                            filePerms = open("/synak_ms/wp_res/webpanel.permissions", "r")
                            # Read the file
                            infoPerms = filePerms.read()
                            # Parse the json
                            jsonPerms = json.loads(infoPerms)
                        # The file cannot be opened or the Json is not valid, stop the script and push an error message to the client
                        except Exception as e:
                            sk__dbg.message(sk__dbg.messtype.ERR, f"An error occured on the permissions file (/synak_ms/wp_res/webpanel.permissions): {str(e)}")
                        # Push an error message to the client if the user does not have permissions to execute this script, else continue the script
                        else:
                            # Declare and initialize variable storing each request check
                            bValidLog = False
                            bValidPwd = False
                            bValidReq = False
                            # Try to check if the request is valid (i.e. login, password, permissions)
                            try:
                                # Check if the login is valid
                                if dicCredentials['sk_log'] in jsonPerms:
                                    bValidLog = True
                                # Check if the password is valid
                                if dicCredentials['sk_pwd'] == str(sha256((jsonPerms[dicCredentials['sk_log']][0] + 'SYNAK_wp').encode('utf-8')).hexdigest()):
                                    bValidPwd = True
                                # Check if the user has the permission for this request
                                if file_name in jsonPerms[dicCredentials['sk_log']][1]:
                                    bValidReq = True
                            # At least one check failed
                            except:
                                pass
                            # The request is valid (i.e. login, password, permissions)
                            finally:
                                # The login and/or password failed
                                if bValidLog == False or bValidPwd == False :
                                    sk__dbg.message(sk__dbg.messtype.PRM, f"Wrong username and/or password.")
                                    sk_mod_bani.process(json.dumps([html.escape(os.environ["REMOTE_ADDR"])]), False)
                                    return
                                # The user has not the permission for this request
                                if bValidLog == False:
                                    sk__dbg.message(sk__dbg.messtype.PRM, f"You do not have the necessary permissions to access this feature ({file_name}).")
                                    return
                                # Script doesn't exist
                                if file_name not in file_dict:
                                    sk__dbg.message(sk__dbg.messtype.ATT, f"script filename does not exist ({file_name}).")
                                # Exec the Prepare() function
                                elif jsonPost["type"] == "prep":
                                    file_dict[file_name].prepare(jsonPost['data'])
                                # Exec the Process() function
                                elif jsonPost["type"] == "proc":
                                    file_dict[file_name].process(jsonPost['data'])
                                # Filename exists, but not the provided type
                                else:
                                    sk__dbg.message(sk__dbg.messtype.ATT, "Type request undefined.")

sk__req()