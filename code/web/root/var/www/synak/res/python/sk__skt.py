#!/usr/bin/python3

import sys
import socket
import json
import struct

import sk__dbg
import sk__res


sys.path.insert(0, '/var/www/synak/dep/cholcombe973')
from crc32 import CRC32


# Send request to the Synak Master Server
def send(_dictData, _arrKeysExpected):
  # Create IPv6 socket
  sockfd = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
  # Enable IPv4-mapped IPv6 IPs
  sockfd.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
  # Throw an error if MS does not answer in 5 seconds
  sockfd.settimeout(5.0)

  # Connect to MS
  try:
    sockfd.connect(('localhost', 45318))
  # Socket cannot connect to MS, send an error message to client
  except:
    sk__dbg.message(sk__dbg.messtype.NFO, "Master Server seems offline")
    return "null", True
  # Socket successfully connected to MS
  else:
    # Encode array to json
    MESSJSN = json.dumps(_dictData)
    # Calculate checksum
    CKSMSND = CRC32(type="CRC-32C").calc(MESSJSN)
    # String to bytes
    MESSJSN = MESSJSN.encode()
    # Send size in network-endianness
    MESSLEN = len(MESSJSN)
    MESSLEN = struct.pack("!I", MESSLEN)
    sockfd.send(MESSLEN)
    # Send checksum in network-endianness
    CKSMSND = struct.pack("!I", CKSMSND)
    sockfd.send(CKSMSND)
    # Send message
    sockfd.send(MESSJSN)
    BUFFER_SIZE = 0
    # Receive answer
    try:
      # Receive buffer size
      BUFFER_SIZE = sockfd.recv(4)
      # Cast to host-endianness
      BUFFER_SIZE = struct.unpack("=I", BUFFER_SIZE)[0]
      # Receive checksum
      CKSMRECV = sockfd.recv(4)
      # Cast to host-endianness
      CKSMRECV = struct.unpack("=I", CKSMRECV)[0]
      # Receive data
      DATA = sockfd.recv(BUFFER_SIZE)
      DATA = DATA.decode()
      sockfd.close()
    # MS does not answer
    except Exception as e:
      sk__dbg.message(sk__dbg.messtype.ATT, f"Master Server does not respond ({str(e)}).")
      return "null", True
    # MS does answer
    else:
      # Checking Json validity
      try:
        DATA = json.loads(DATA)
      except Exception as e:
        sk__dbg.message(sk__dbg.messtype.ERR, f"Json is not valid ({str(e)}) ({DATA}).")
        return "null", True
      else:
        # All expected keys are in the json received
        if all(elem in DATA["data"] for elem in _arrKeysExpected):
          # Verifying checksum
          CKSMRECV_VERIF = CRC32(type="CRC-32C").calc(str(DATA))
          if CKSMRECV_VERIF != CKSMRECV :
            return DATA, False
          else:
            sk__dbg.message(sk__dbg.messtype.ERR, f"Checksum not valid. CALC({CKSMRECV_VERIF}) != RECV({CKSMRECV})")
            return "null", True
        # At least one expected argument is missing
        else:
          sk__dbg.message(sk__dbg.messtype.ERR, "At least one expected argument is missing from Master Server answer.")
          return "null", True
      
