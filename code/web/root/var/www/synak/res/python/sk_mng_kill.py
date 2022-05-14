#!/usr/bin/python3

import sk__cmd
import sk__res
import sk__dbg
import sk__mng
import sk__opn

# Push the modal disclaimer about killing the MS process
def prepare(_data):
    # Get MS PID
    pid = sk__mng.getPid(False)
    # MS is not running, push error message to client
    if pid == 0:
        sk__dbg.message(sk__dbg.messtype.NFO, "Master Server is not running")
    # MS is running
    else:
        # Get the whole MS process tree
        proctree = sk__cmd.send("pstree -a -U -c -n -p | grep synak_ms | grep -v 'grep\|pstree'")
        # Replace terminal to web new line
        proctree = proctree.replace('\n', '<br/>')
        # Get the segment template
        template_raw = sk__opn.getTemplate("sk_mng_kill")
        # Fill template with MS process tree
        template_mod = template_raw.replace("%PROC_TREE%", proctree)
        sk__res.show("prep", template_mod)

# Push segment to client
def process(_data):
    # Get MS PID
    pid = sk__mng.getPid(False)
    # MS has been shut down in the meantime, push error message to client
    if pid == 0:
        sk__dbg.message(sk__dbg.messtype.ATT, "It seems that no Master Server was running")
    # MS is running
    else:
        # Send OS SIGKILL signal to the MS process
        sk__cmd.send(f"sudo kill -9 {pid}")
        # Get the MS PID
        pid = sk__mng.getPid(True)
        # MS has been successfully shut down, push success message to client
        if pid == 0:
            sk__dbg.message(sk__dbg.messtype.SUC, "Master Server has been <b>STOPPED</b> successfully")
        # There is still at least 1 MS process running, push error message to client
        else:
            sk__dbg.message(sk__dbg.messtype.ERR, "Master Server is still running")
