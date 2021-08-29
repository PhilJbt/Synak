#!/usr/bin/python3

from enum import Enum

class debug_messtype(Enum):
    ERROR = 0, 'red">ERROR</a>'
    INFO  = 1, 'blue">INFO</a>'

    def __new__(cls, value, name):
        member = object.__new__(cls)
        member._value_   = value
        member.fullname  = name
        return member

    def __int__(self):
        return self.value

def debug_message(debugtype, message):
  string = "<a class=\"ui circular label " + debugtype.fullname + " " + message
  return string