#!/usr/bin/python3

import sys
import select
import json

import sk__dbg
import sk_mng_srt
import sk_mng_stp
import sk_mng_kll
import sk_mod_ban
import sk_mod_unb
import sk_log_get
import sk_log_era
#import sk_cfg_rel
#import sk_stt_sms
import sk_stt_ded

try:
  dataJson = json.load(sys.stdin)
except:
  sk__dbg.message(sk__dbg.messtype.ATT, "request undefined")
else:
  file_dict = {
    'sk_mng_srt' : sk_mng_srt,
    'sk_mng_stp' : sk_mng_stp,
    'sk_mng_kll' : sk_mng_kll,
    'sk_mod_ban' : sk_mod_ban,
    'sk_mod_unb' : sk_mod_unb,    
    'sk_log_get' : sk_log_get,
    'sk_log_era' : sk_log_era,
    #'sk_cfg_rel' : sk_cfg_rel,
    #'sk_stt_sms' : sk_stt_sms,
    'sk_stt_ded' : sk_stt_ded,
  }
  file_name = dataJson["file"]
  if file_name not in file_dict:
    sk__dbg.message(sk__dbg.messtype.ATT, "script filename does not exist")
  elif dataJson["type"] == "prep":
    file_dict[file_name].prepare(dataJson['data'])
  elif dataJson["type"] == "proc":
    file_dict[file_name].process(dataJson['data'])
  else:
    sk__dbg.message(sk__dbg.messtype.ATT, "type request undefined")
