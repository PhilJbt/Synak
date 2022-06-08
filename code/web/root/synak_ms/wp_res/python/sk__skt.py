#!/usr/bin/python3

import sys
import socket
import json
import struct
import zlib

import sk__dbg
import sk__res


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
    except Exception as err:
        # Connection refused
        if err.errno == 111:
            sk__dbg.message(sk__dbg.messtype.NFO, f"Master Server seems offline.")
        else:
            sk__dbg.message(sk__dbg.messtype.ERR, f"Master Server connection failed:<br/><b>{str(err)}</b>")
        return None, True
    # Socket successfully connected to MS
    else:
        # Serialize python array to json, then to byte array
        MESSBYT = json.dumps(_dictData).encode()
        # Calculate size
        MESSLEN = len(MESSBYT)
        MESSLEN = MESSLEN.to_bytes(4, 'little')
        # Calculate checksum (network-endianness)
        MESSFUL = b''.join([MESSLEN, MESSBYT])
        CKSMSND = zlib.crc32(MESSFUL)
        CKSMSND = struct.pack("!I", CKSMSND)
        # Cast length int to byte array (network-endianness)
        MESSLEN = struct.pack("!I", int.from_bytes(MESSLEN, "little"))
        # Send message
        sockfd.send(CKSMSND + MESSLEN + MESSBYT)
        # Receive answer
        try:
            # Receive checksum
            CKSMRECV = sockfd.recv(4)
            # The Master Server did not answer
            if CKSMRECV == b'':
                sk__dbg.message(sk__dbg.messtype.ERR, "The Master Server is online but did not answer.")
                return None, True
            # Cast to host-endianness
            CKSMRECV = struct.unpack("!I", CKSMRECV)[0]
            # Receive buffer size
            BUFFER_SIZE = sockfd.recv(4)
            # Cast to host-endianness
            BUFFER_SIZE = struct.unpack("!I", BUFFER_SIZE)[0]
            # The data length exceed the limit
            if BUFFER_SIZE > 5242880:
                sk__dbg.message(sk__dbg.messtype.ERR, f"The data to receive exceed the 5 Megabytes maximum limit. ({BUFFER_SIZE})")
                return None, True
            # Receive data
            DATA = sockfd.recv(BUFFER_SIZE)
            sockfd.close()
        # MS does not answer
        except Exception as e:
            sk__dbg.message(sk__dbg.messtype.ATT, f"Master Server does not respond ({str(e)}).")
            return None, True
        # MS does answer
        else:
            # Verifying checksum
            MESSFUL = b''.join([BUFFER_SIZE.to_bytes(4, 'big'), DATA])
            CKSMRECV_VERIF = zlib.crc32(MESSFUL)
            if CKSMRECV_VERIF != CKSMRECV :
                sk__dbg.message(sk__dbg.messtype.ERR, f"Checksum not valid. CALC({CKSMRECV_VERIF}) != RECV({CKSMRECV})")
                return None, True
            # Checking Json validity
            try:
                DATA = json.loads(DATA.decode())
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

