**abo-io.exe**

When we open this ABO in IDA we can see that it receives 2 arguments

![](media/dec095c3df56ccceadf1927f3fc04def.png)

![](media/e110d4a66d08632af6d49ba0df87a50a.png)

The **sscanf()**  read formatted data from a string.

int sscanf(

const char \*buffer,

const char \*format [,

argument ]

In the main block we can see how the variables are represented in the stack.

![Texto Descripción generada automáticamente con confianza media](media/ce10d8db9160ae5a682f482f934c5d97.png)

Here **sscanf**() function reads input data from a buffer in this case argv1

![Interfaz de usuario gráfica, Texto, Aplicación Descripción generada automáticamente](media/82e660bea120a370e3b50e7e3e3a48c7.png)

The format of arg1 corresponds to unsigned integer (**%u**), with this we deduce that the first argument that we must pass is an integer

![Interfaz de usuario gráfica, Texto, Aplicación, Correo electrónico Descripción generada automáticamente](media/23b7523a7dd60a3af4bcdc5696a8335f.png)

Then calculates the size of the second argument string (**argv2**)

![](media/6bcb82ecff696b85703d286b0b48269d.png)

After calculating the size of the second argument (argv2) perform the following operations:

![Interfaz de usuario gráfica, Texto Descripción generada automáticamente](media/1a2c91fc2181c46974e814906feee309.png)

**buffer + offset \* 4 + len(argv2)**

So, in order to reach \_**strcpy()**, the condition in the image above must be met, that is, the result of the operations performed just before must be **EAX** \<= to the value of **EDX**

![A screenshot of a computer Description automatically generated](media/bed8d53964bbfcc80ae7b7d2196ff919.png)

When it reaches \_**strcpy()**, it will use **buffer+offset\*4** as destination buffer, remember that the buffer size is 255 bytes

![Interfaz de usuario gráfica, Texto Descripción generada automáticamente](media/6b0880115a076eeec5887348ad9cdf92.png)

If we look at the distance from the buffer variable to the return address, we can see that it is 268 bytes.

![Interfaz de usuario gráfica, Aplicación Descripción generada automáticamente](media/4840ff22e6b716f22ee753e75092e20e.png)

So we know that the destination address where memcpy will write comes from the result of **buffer + offset \* 4**

Since **offset** corresponds to the first argument which we control, we can also control the destination where the **memcpy()** function will copy.

![Interfaz de usuario gráfica, Aplicación Descripción generada automáticamente](media/88c5d8672ea58d151d4acf24f6d2e53f.png)

compares if the final result exceeds the beginning of the next variable placed on the stack that follows it, in this case it is **un_byte**

![Interfaz de usuario gráfica, Texto, Aplicación Descripción generada automáticamente](media/8c635f68be6a425c0d00c2d791582c50.png)

Here we conclude on the importance of the length of the second argument (**argv[2]**)

On the other hand, the maximum size of the argv[2] string cannot exceed 255-4 which is the buffer size.

Taking this into account, we would not be able to reach the return address, we would be missing 12 bytes as seen in the image.

![Interfaz de usuario gráfica, Texto Descripción generada automáticamente con confianza media](media/f584f0519d3731fb476f9acc850794ba.png)

The solution in this case would be to send a negative value in the first argument (argv[1]) and a long string (up to 255) so that when the multiplication and addition are performed, the result is a smaller value that passes the comparison. The advantage is that we can control both the value of argv[1] and the string of argv[2] so that we can find the correct values ​​to be able to step on the return address.

Remember that the destination address of memcpy came from this formula:

**buffer + offset**(argv[1]**) \* 4**

Let's try these values:

Offset(argv[1]) = -**63** len(argv[2])= **255** ==\> Destination: 19FD3C

The result it’s a buffer overflow

We note that we control the ESI, EDI, EIP, EBP registers and eax points to the destination buffer of **strcpy()**

![Interfaz de usuario gráfica, Aplicación Descripción generada automáticamente](media/c8a208185ec68c1408c2b649ad839bd5.png)

![Calendario Descripción generada automáticamente con confianza media](media/818a7a4a7dd6afd2b663606927a22e5e.png)

![Tabla Descripción generada automáticamente con confianza media](media/c70c0a9385934d6255317b40da6d2107.png)

In ESP+4 is the address of argv2, so we can make it jump there to execute code, and thus have the entire shellcode complete.

![Interfaz de usuario gráfica, Texto, Aplicación, Word Descripción generada automáticamente](media/b16dd7eee351aaa2b18720f2827fd31a.png)

We need to pop a value from the stack in order to jump to our code, so we look for a pop-ret

![](media/d9efada304d0aa3cd1421682ae5ae1b6.png)

This is what our shellcode looks like in assembler

![Interfaz de usuario gráfica Descripción generada automáticamente con confianza media](media/47d4c1f61b8a2e6b652206f9ea088b1a.png)

The script:

![A screenshot of a computer program Description automatically generated](media/e06b20392e89abfcf907872abbf0c6db.png)
