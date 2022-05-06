#!/usr/bin/python3

import json

# Send DATA or HTML to the client
def show(_type, _data):
  data = {
    "type": _type,
    "data": _data
  }
  print("Content-type: text/html\n")
  print(json.dumps(data))
