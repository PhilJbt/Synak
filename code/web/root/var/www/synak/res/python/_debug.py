#!/usr/bin/python3

from enum import Enum

class debug_messtype(Enum):
    ERR = 0, "ERROR",       "red",    "exclamation"
    ATT = 1, "ATTENTION",   "yellow", "exclamation triangle"
    NFO = 2, "INFORMATION", "blue",   "info circle"

    def __new__(_cls, _value, _title, _color, _icon):
        member = object.__new__(_cls)
        member._value_ = _value
        member._title_ = _title
        member._color_ = _color
        member._icon_  = _icon
        return member

    def __int__(_self):
        return _self._value

def debug_message(_debugtype, _message):
  string = '<div class="ui icon message ' + _debugtype._color_ + '"> <i class="close icon"></i><i class="' + _debugtype._icon_ + ' icon"></i><div class="content"><div class="header">'
  string += _debugtype._title_ + '</div><p>'
  string += _message + '</p></div></div>'
  return string