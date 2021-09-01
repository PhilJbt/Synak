#!/usr/bin/python3

import sk__cmd

def getPid():
  return sk__cmd.send("sudo ps aux | grep synak_ms.bin | grep -v 'tmux\|grep' | awk '{print $2}'")