#!/usr/bin/python3

import sys
import json
import subprocess

import sk__cmd
import sk__res
import sk__skt
import sk__dbg

def process():
  res = subprocess.check_output('pstree -p  | grep "f2b"', shell=True).decode("utf-8") 
  sk__res.show("proc", res)
