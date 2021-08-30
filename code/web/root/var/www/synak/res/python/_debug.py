#!/usr/bin/python3

from enum import Enum

class debug_messtype(Enum):
    ERR = 0, "ERROR",       "red",    "exclamation"
    ATT = 1, "ATTENTION",   "yellow", "exclamation triangle"
    NFO = 2, "INFORMATION", "blue",   "info circle"

    def __new__(cls, value, title, color, icon):
        member = object.__new__(cls)
        member._value_ = value
        member._title_ = title
        member._color_ = color
        member._icon_  = icon
        return member

    def __int__(self):
        return self.value

def debug_message(debugtype, message):
  string = '<div class="ui icon message ' + debugtype._color_ + '"> <i class="close icon"></i><i class="' + debugtype._icon_ + ' icon"></i><div class="content"><div class="header">'
  string += debugtype._title_ + '</div><p>'
  string += message + '</p></div></div>'
  return string