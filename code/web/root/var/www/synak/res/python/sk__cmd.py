#!/usr/bin/python3

import subprocess

import sk__dbg

def send(_cmd):
  output = subprocess.Popen(_cmd, shell=True, universal_newlines=True, stdout=subprocess.PIPE)
  out, err = output.communicate()
  if err:
    sk__dbg.message(sk__dbg.messtype.NFO, "The command '" + _cmd + "' triggered an error: " + err)
  else:
    return out
