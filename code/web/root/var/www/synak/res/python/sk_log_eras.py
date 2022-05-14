#!/usr/bin/python3

import sys
import json
import os.path
from datetime import datetime

import sk__cmd
import sk__res
import sk__dbg
import sk__opn

# Push the Log erase modal to the client
def prepare(_data):
    # Get the ban modal template
    template_raw = sk__opn.getTemplate("sk_log_eras")
    # Send the modal to the client
    sk__res.show("prep", template_raw)

# Push segment to client
def process(_data):
    if os.path.exists('/synak_ms/synak_ms.log'):
        # Get current time
        timeCurr = datetime.now().strftime("%H:%M:%S %d/%m/%Y")

        # Write in log file
        try:
            file_object = open('/synak_ms/synak_ms.log', 'w')
            file_object.write(f'["1","NFO","N/A 0","{timeCurr}", ["Log has been erased."]]')
            file_object.close()
            sk__dbg.message(sk__dbg.messtype.SUC, 'Log file "/synak_ms/synak_ms.log" erased.')
        except Exception as e:
            sk__dbg.message(sk__dbg.messtype.ERR, f'Log file "/synak_ms/synak_ms.log" cannot be erased: {e}.')
    else:
        sk__dbg.message(sk__dbg.messtype.ERR, 'Log file "/synak_ms/synak_ms.log" does not exist.')
