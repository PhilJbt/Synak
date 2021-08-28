#!/usr/bin/python3

import subprocess

def command_send(cmd):
  output = subprocess.Popen(cmd.split(), universal_newlines=True, stdout=subprocess.PIPE)
  out, err = output.communicate()
  return out.splitlines()[0], bool(err), err

def command_check(output, unvalid, err):
  if unvalid:
    print("err")
    return True
  else:
    return False