#!/usr/bin/python3

import time

import sk__cmd

# Send a command to unix terminal to retrieve MS PID
def cmdPid():
    chk, res = sk__cmd.send("sudo ps aux | grep synak_ms.bin | grep -v 'tmux\|grep' | awk '{print $2}'")
    if chk == False:
        return
    return res

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
        iLoop = 0
        iSleep = .33
        while iLoop < 3:
            # Wait for n ms
            time.sleep(iSleep)
            # Get MS PID again
            pid = checkPid()
            # Wait a little longer if the result is not equal as expected before return the result
            if ((_bZeroExpected == True) and (pid == 0)) or ((_bZeroExpected == False) and (pid > 0)):
                iLoop = 9
            iLoop += 1
            iSleep += (iLoop * 0.33)
        # Send the latter to the client
        return pid