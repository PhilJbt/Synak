#!/usr/bin/python3

import sys
import json
import subprocess

import sk__cmd
import sk__res
import sk__skt

def prepare():  
  file = open("../template/sk_mod_ban.tpl", "r")
  template_raw = file.read()
  template_mod = template_raw.replace("%VAR_1%", "test")
  sk__res.show("prep", template_mod)

def process():
  res, err = sk__skt.send()
  if not err:
    sk__res.show("proc", res)

dataI = json.load(sys.stdin)
if dataI["type"] == "prep":
  prepare()
elif dataI["type"] == "proc":
  process()