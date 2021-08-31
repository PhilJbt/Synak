#!/usr/bin/python3

from _command import *
from _result import *

import sys
import json
import subprocess

def log_get_Pprepare():  
  file = open("../template/log_get.tpl", "r")
  template_raw = file.read()
  template_mod = template_raw.replace("%VAR_1%", "test")
  dataO = {
    "type": "prep",
    "data": template_mod
  }
  result_show(json.dumps(dataO))

def log_get_Pprocess():
  res = subprocess.check_output('pstree -p  | grep "f2b"', shell=True).decode("utf-8") 
  dataO = {
    "type": "proc",
    "data": res
  }
  result_show(json.dumps(dataO))

dataI = json.load(sys.stdin)
if dataI["type"] == "prep":
  log_get_Pprepare()
elif dataI["type"] == "proc":
  log_get_Pprocess()