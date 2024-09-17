# ABO collection

ABO (Advanced Buffer Overflow) originally created by [Gerardo Richarte](https://github.com/gerasdf/InsecureProgramming), it is a series of exercises and solutions specially created to understand and exploit the different kind of most common vulnerabilities.
Over time more techniques were added to the exercises, not only buffer overflows, also it was updated to the latest Windows Operating systems.


**Stacks:** These exercises serve to become familiar with the tools, learn how the stack works, delve into assembly language, the hexadecimal number system, the "little endian" convention, among other thing

**Abos:** This section is the next step after solving the STACKS exercises, increasing the difficulty by looking at memory corruptions such as Heap Overflow, Integer Overflow, and ROP techniques to bypass DEP (Data Execution Prevention).

**Remote:**  To continue practicing and learning how to exploit memory corruption vulnerabilities in general, with the addition of starting to work with remote connections by sending packets through sockets. 
This section is interesting since with it we will be able to execute code remotely without the need for interaction from another user.

**Advanced ABOs:** Here the difficulty increases and more complex vulnerabilities are dealt with, such as Use-After-Free and integer overflow, and some system mitigation may also be added.

To solve the problems, it is recommended to use the following tools:
- IDA / X64dbg
- Windbg
- Python
- HxD
- Visual Studio
