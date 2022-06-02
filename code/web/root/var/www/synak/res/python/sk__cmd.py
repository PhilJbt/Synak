#!/usr/bin/python3

import subprocess

import sk__dbg

# Function to send a command to a unix terminal
def send(_cmd):
    # Send the command to a terminal
    try:
        output = subprocess.Popen(_cmd, shell=True, text=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = output.communicate()
    except OSError as err:
        sk__dbg.message(sk__dbg.messtype.ERR, f"The command '{_cmd}' triggered an OSError:<br/><b>{str(err)}</b>")
        return False, ''
    except Exception as err:
        sk__dbg.message(sk__dbg.messtype.ERR, f"The command '{_cmd}' triggered an Exception:<br/><b>{str(err.message)}</b>")
        return False, ''

    # If an error occurs, show an error message
    if output.returncode != 0:
        sk__dbg.message(sk__dbg.messtype.ERR, f"The command '{_cmd}' triggered an error:<br/><b>{str('Unknown error.' if err is None else err)}</b>")
        return False, ''
    # Else, return the output
    else:
        return True, out.strip()
