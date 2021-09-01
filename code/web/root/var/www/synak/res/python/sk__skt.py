#!/usr/bin/python3

import socket
import json

import sk__dbg
import sk__res

def send():
  sockfd = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
  sockfd.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
  sockfd.settimeout(5.0)

  try:
    sockfd.connect(('localhost', 45318))
  except:
    sk__dbg.message(sk__dbg.messtype.NFO, "Master Server seems offline")
    return "null", True
  else:
    MESSAGE = "{\
    \"co_tpe\": \"connection\",\
    \"co_act\": 1\
    }".encode()
    sockfd.send(MESSAGE)
    BUFFER_SIZE = 2048

    try:
      data = sockfd.recv(BUFFER_SIZE)
      sockfd.close()
    except:
      sk__dbg.message(sk__dbg.messtype.ATT, "Master Server does not respond")
      return "null", True
    else:
      jRecv = json.loads(data.decode())
      if {'valid', 'port'} <= set(jRecv):
        result = "valid: " + str(jRecv["valid"]) + "\nport:" + str(jRecv["port"])
        return result, False
      else:
        sk__dbg.message(sk__dbg.messtype.ERR, "valid or port arg unknown")
        return "null", True
