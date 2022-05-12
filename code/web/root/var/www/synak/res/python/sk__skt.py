#!/usr/bin/python3

import sys
import socket
import json
import struct

import sk__dbg
import sk__res


sys.path.insert(0, '../../dep/cholcombe973')
from crc32 import CRC32


# Function to send a request to the Synak Master Server
def send(_dictData, _arrKeysExpected = None):
  # Get the Synak Master Server config file (created at startup)
  try:
    cfg_startup = open("/synak_ms/synak_ms.cfg", "r")
    jsn_startup = json.load(cfg_startup)
  except Exception as e:
    sk__dbg.message(sk__dbg.messtype.ERR, f'Synak Master Server config file error ("/synak_ms/synak_ms.cfg", created at startup) : {e}')
    return None, True

  # Create IPv6 socket
  sockfd = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
  # Enable IPv4-mapped IPv6 IPs
  sockfd.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
  # Throw an error if MS does not answer in 5 seconds
  sockfd.settimeout(5.0)

  # Connect to MS
  try:
    sockfd.connect(('localhost', int(jsn_startup['ptwp'])))
  # Socket cannot connect to MS, send an error message to client
  except:
    sk__dbg.message(sk__dbg.messtype.NFO, "Master Server seems offline")
    return None, True
  # Socket successfully connected to MS
  else:
    # Serialize array to json
    MESSJSN = json.dumps(_dictData)
    # Calculate checksum (network-endianness)
    CKSMSND = CRC32(type="CRC-32C").calc(MESSJSN)
    CKSMSND = struct.pack("!I", CKSMSND)
    # String to bytes array
    MESSJSN = MESSJSN.encode()
    # Calculate size (network-endianness)
    MESSLEN = len(MESSJSN)
    MESSLEN = struct.pack("!I", MESSLEN)
    # Send message
    sockfd.send(MESSLEN + CKSMSND + MESSJSN)
    # Receive answer
    try:
      # Receive buffer size
      BUFFER_SIZE = sockfd.recv(4)
      # Cast to host-endianness
      BUFFER_SIZE = struct.unpack("!I", BUFFER_SIZE)[0]
      # Receive checksum
      CKSMRECV = sockfd.recv(4)
      # Cast to host-endianness
      CKSMRECV = struct.unpack("!I", CKSMRECV)[0]
      # Receive data
      DATA = sockfd.recv(BUFFER_SIZE)
      DATA = DATA.decode()
      sockfd.close()
    # MS does not answer
    except Exception as e:
      sk__dbg.message(sk__dbg.messtype.ATT, f"Master Server does not respond ({str(e)}).")
      return None, True
    # MS does answer
    else:
      # Verifying checksum
      CKSMRECV_VERIF = CRC32(type="CRC-32C").calc(str(DATA))
      if CKSMRECV_VERIF != CKSMRECV :
        sk__dbg.message(sk__dbg.messtype.ERR, f"Checksum not valid. CALC({CKSMRECV_VERIF}) != RECV({CKSMRECV})")
        return None, True
      # Checking Json validity
      try:
        DATA = json.loads(DATA)
      except Exception as e:
        sk__dbg.message(sk__dbg.messtype.ERR, f"Json is not valid ({str(e)}) ({DATA}).")
        return None, True
      # Check that the master server has not encountered any errors
      if DATA['type'] == 'erro':
        sk__res.show('erro', DATA['data'])
        return None, True
      # Bypass arg return if no arg expected
      strCond = '1'
      if _arrKeysExpected != None:
        strCond = f'all(elem in {DATA["data"]} for elem in {_arrKeysExpected})'
      # All expected keys are in the json received
      if eval(strCond):
        return DATA, False
      # At least one expected argument is missing
      else:
        sk__dbg.message(sk__dbg.messtype.ERR, "At least one expected argument is missing from Master Server answer.")
        return None, True

