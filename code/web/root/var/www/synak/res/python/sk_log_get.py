#!/usr/bin/python3

import sk__cmd
import sk__res
import sk__skt

import sys
import json
import subprocess

def prepare():  
  file = open("../template/sk_log_get.tpl", "r")
  template_raw = file.read()
  template_mod = template_raw.replace("%VAR_1%", "test")
  sk__res.show("prep", template_mod)

def process():
  res = subprocess.check_output('pstree -p  | grep "f2b"', shell=True).decode("utf-8") 
  sk__res.show("proc", res)

dataI = json.load(sys.stdin)
if dataI["type"] == "prep":
  prepare()
elif dataI["type"] == "proc":
  process()