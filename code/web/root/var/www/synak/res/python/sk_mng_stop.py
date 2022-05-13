#!/usr/bin/python3

import signal

import sk__cmd
import sk__res
import sk__dbg
import sk__mng

# Push the modal disclaimer about killing the MS process
def prepare(_data):
    # Get MS PID
    pid = sk__mng.getPid(False)
    # There is no MS process running, push an info message to client
    if pid == 0:
        sk__dbg.message(sk__dbg.messtype.NFO, "Master Server is not running")
    # A MS process is running
    else:
        # Get the modal stop template
        file = open("../template/sk_mng_stop.tpl", "r")
        template_raw = file.read()
        # Push the modal to the client
        sk__res.show("prep", template_raw)

# Push segment to client
def process(_data):
    # Get the MS PID
    pid = sk__mng.getPid(False)
    # MS has been shut down in the meantime, push error message to client
    if pid == 0:
        sk__dbg.message(sk__dbg.messtype.ATT, "It seems that no Master Server was running")
    # MS process is running
    else:
        # Send OS SIGUSR1 signal to the MS process, triggering a clean shut down
        sk__cmd.send(f"sudo kill -{signal.SIGUSR1} {pid}")
        # Get MS PID
        pid = sk__mng.getPid(True)
        # There is no MS process running anymore, push a success message to client
        if pid == 0:
            sk__dbg.message(sk__dbg.messtype.SUC, "Master Server has been <b>STOPPED</b> successfully")
        # There is still at least 1 MS process running, push an error message to the client
        else:
            sk__dbg.message(sk__dbg.messtype.ERR, "Master Server is still running")
