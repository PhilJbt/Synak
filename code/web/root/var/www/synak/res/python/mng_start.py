#!/usr/bin/python3

from _command import *
from _result import *

def mng_start():
  output, unvalid, err = command_send("date +%T:%N")
  if not command_check(output, unvalid, err):
    html = "<div style=\"background-color:blue;\">" + output + "</div>"
    result_show(html)

mng_start()