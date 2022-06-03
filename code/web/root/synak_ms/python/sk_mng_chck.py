#!/usr/bin/python3

import sk__res
import sk__mng
import sk__opn

# get the MS process ID and push the result to the client
def prepare(_data):
    # Get MS PID
    pid = sk__mng.getPid(False)
    # MS is not running, push error message to client
    if pid == 0:
        # Get templates, and push to client
        htmlTemplate = sk__opn.getTemplate("sk_log_chck_offline")
        sk__res.show("proc", htmlTemplate)
    # MS is running
    else:
        # Get templates, and push to client
        htmlTemplate = sk__opn.getTemplate("sk_log_chck_online")
        sk__res.show("proc", htmlTemplate)
