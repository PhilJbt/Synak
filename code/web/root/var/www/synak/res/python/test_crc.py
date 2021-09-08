#!/usr/bin/python3

import sys
sys.path.insert(0, '/var/www/synak/dep/cholcombe973')
from crc32 import CRC32

TESTRING = "qzodkqpmzdkopqmkzd"
checksum = CRC32(type="CRC-32C").calc(TESTRING)

print("Content-type: text/html\n")
print(checksum)