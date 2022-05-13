#!/usr/bin/python3

import sk__res
import sk__mng

# get the MS process ID and push the result to the client
def prepare(_data):
    # Get MS PID
    pid = sk__mng.getPid(False)
    # MS is not running, push error message to client
    if pid == 0:
        # Get templates, and push to client
        fTemplate = open("../template/sk_log_chck_offline.tpl", "r")
        htmlTemplate = fTemplate.read()
        sk__res.show("proc", htmlTemplate)
    # MS is running
    else:
        # Get templates, and push to client
        fTemplate = open("../template/sk_log_chck_online.tpl", "r")
        htmlTemplate = fTemplate.read()
        sk__res.show("proc", htmlTemplate)
