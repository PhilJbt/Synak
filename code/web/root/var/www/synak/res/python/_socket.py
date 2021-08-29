#!/usr/bin/python3

import socket
import json

def socket_send():
  sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sockfd.connect((socket.gethostbyname(socket.gethostname()), 45318))
  sockfd.settimeout(5.0)

  MESSAGE = "{\
  \"co_tpe\": \"connection\",\
  \"co_act\": 1\
  }".encode()
  sockfd.send(MESSAGE)

  BUFFER_SIZE = 2048
  data = sockfd.recv(BUFFER_SIZE)
  sockfd.close()

  jRecv = json.loads(data.decode())
  print("Content-type: text/html\n")
  print("valid: %s\n" % (jRecv["valid"]))
  print("port: %s\n" % (jRecv["port"]))


socket_send()