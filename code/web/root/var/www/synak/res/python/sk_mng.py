#!/usr/bin/python3

import time

import sk__cmd

def cmdPid():
  return sk__cmd.send("sudo ps aux | grep synak_ms.bin | grep -v 'tmux\|grep' | awk '{print $2}'")

def checkPid():
  pid = cmdPid()
  try:
    pid = int(pid)
  except ValueError:
    pid = 0
  return pid

def getPid(_bZeroExpected):
  pid = checkPid()
  if ((_bZeroExpected == True) and (pid == 0)) or ((_bZeroExpected == False) and (pid > 0)):
    return pid
  else:
    time.sleep(3.0)
    pid = checkPid()
    return pid