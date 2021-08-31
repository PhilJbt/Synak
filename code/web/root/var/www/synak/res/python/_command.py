#!/usr/bin/python3

import subprocess

def command_send(_cmd):
  output = subprocess.Popen(_cmd.split(), universal_newlines=True, stdout=subprocess.PIPE)
  out, err = output.communicate()
  return out.splitlines()[0], bool(err), err

def command_check(_output, _unvalid, _err):
  if unvalid:
    print("err")
    return True
  else:
    return False