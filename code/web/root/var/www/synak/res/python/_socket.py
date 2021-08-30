#!/usr/bin/python3

import socket
import json
from _debug import *
from _result import *

def socket_send():
  sockfd = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
  sockfd.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
  sockfd.settimeout(5.0)

  try:
    sockfd.connect(('localhost', 45318))
  except:
    result_show(debug_message(debug_messtype.NFO, "Master Server seems offline"))
  else:
    MESSAGE = "{\
    \"co_tpe\": \"connection\",\
    \"co_act\": 1\
    }".encode()
    sockfd.send(MESSAGE)

    try:
      BUFFER_SIZE = 2048
      data = sockfd.recv(BUFFER_SIZE)
      sockfd.close()
    except:
      result_show(debug_message(debug_messtype.ATT, "Master Server does not respond"))
    else:
      jRecv = json.loads(data.decode())
      if {'valid', 'port'} <= set(jRecv):
        result = "valid: " + str(jRecv["valid"]) + "\nport:" + str(jRecv["port"])
        result_show(result)
      else:
        result_show(debug_message(debug_messtype.ERROR, "valid or port arg unknown"))

socket_send()