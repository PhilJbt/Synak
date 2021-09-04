#!/usr/bin/python3

import time

import sk__cmd

# Send terminal command to OS to retrieve MS PID
def cmdPid():
  return sk__cmd.send("sudo ps aux | grep synak_ms.bin | grep -v 'tmux\|grep' | awk '{print $2}'")

# Check PID value, if unvalid store 0 as PID
def checkPid():
  pid = cmdPid()
  try:
    pid = int(pid)
  except ValueError:
    pid = 0
  return pid

# Retrieve MS PID
def getPid(_bZeroExpected):
  # Get MS PID
  pid = checkPid()
  # Returns the PID value if it is the expected one
  if ((_bZeroExpected == True) and (pid == 0)) or ((_bZeroExpected == False) and (pid > 0)):
    return pid
  # If PID value does not does not match the expected one
  else:
    # Wait for 3 seconds
    time.sleep(3.0)
    # Get MS PID again
    pid = checkPid()
    # Send the latter to the client
    return pid