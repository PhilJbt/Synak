#!/usr/bin/python3

import socket
import json

import sk__dbg
import sk__res

# Send request to the Synak Master Server
def send(_dictData, _arrKeysExpected):
  # Create IPv6 socket
  sockfd = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
  # Enable IPv4-mapped IPv6 IPs
  sockfd.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
  # Throw an error if MS does not answer in 5 seconds
  sockfd.settimeout(5.0)

  # Connect to MS
  try:
    sockfd.connect(('localhost', 45318))
  # Socket cannot connect to MS, send an error message to client
  except:
    sk__dbg.message(sk__dbg.messtype.NFO, "Master Server seems offline")
    return "null", True
  # Socket successfully connected to MS
  else:
    # Encode array to json
    MESSAGE = json.dumps(_dictData).encode()
    # Send
    sockfd.send(MESSAGE)
    BUFFER_SIZE = 2048
    # Receive answer
    try:
      data = sockfd.recv(BUFFER_SIZE)
      sockfd.close()
    # MS does not answer
    except:
      sk__dbg.message(sk__dbg.messtype.ATT, "Master Server does not respond")
      return "null", True
    # MS does answer
    else:
      jRecv = json.loads(data.decode())
      # All expected keys are in the json received
      if all(elem in jRecv["data"] for elem in _arrKeysExpected):
        return jRecv, False
      # At least one expected argument is missing
      else:
        sk__dbg.message(sk__dbg.messtype.ERR, "At least one expected argument is missing from Master Server answer.")
        return "null", True
