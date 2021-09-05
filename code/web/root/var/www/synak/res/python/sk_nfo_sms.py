#!/usr/bin/python3

import sk__res
import sk__skt
from sk_mng import *

# Push segment to client
def process(_data):
  res, err = sk__skt.send()
  if not err:
    sk__res.show("proc", res)