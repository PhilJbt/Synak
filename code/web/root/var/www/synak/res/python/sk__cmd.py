#!/usr/bin/python3

import subprocess

import sk__dbg

def send(_cmd):
  # Send the command to a terminal
  output = subprocess.Popen(_cmd, shell=True, text=True, universal_newlines=True, stdout=subprocess.PIPE)
  out, err = output.communicate()

  # If an error occurs, show an error message
  if err:
    sk__dbg.message(sk__dbg.messtype.NFO, "The command '" + _cmd + "' triggered an error: " + err)
  # Else, return the output
  else:
    return out
