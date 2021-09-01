#!/usr/bin/python3

import json
from enum import Enum

import sk__res

class messtype(Enum):
    ERR = 0, "ERROR",       "red",    "exclamation"
    ATT = 1, "ATTENTION",   "yellow", "exclamation triangle"
    NFO = 2, "INFORMATION", "blue",   "info circle"
    SUC = 3, "SUCCESS", "green",  "check"

    def __new__(_cls, _value, _title, _color, _icon):
        member = object.__new__(_cls)
        member._value_ = _value
        member._title_ = _title
        member._color_ = _color
        member._icon_  = _icon
        return member

    def __int__(_self):
        return _self._value

def message(_debugtype, _message):
  data = {
    "colr": _debugtype._color_,
    "icon": _debugtype._icon_,
    "titl": _debugtype._title_,
    "mess": _message
  }
  sk__res.show("erro", json.dumps(data))
