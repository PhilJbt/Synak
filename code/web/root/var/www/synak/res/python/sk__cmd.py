#!/usr/bin/python3

import subprocess

def send(_cmd):
  output = subprocess.Popen(_cmd.split(), universal_newlines=True, stdout=subprocess.PIPE)
  out, err = output.communicate()
  return out.splitlines()[0], bool(err), err

def check(_output, _unvalid, _err):
  if _unvalid:
    print("err")
    return True
  else:
    return False