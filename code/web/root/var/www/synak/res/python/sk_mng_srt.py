#!/usr/bin/python3

import sk__cmd
import sk__res

def prepare():
  output, unvalid, err = sk__cmd.send("date +%T:%N")
  if not sk__cmd.check(output, unvalid, err):
    sk__res.show("proc", output)

prepare()