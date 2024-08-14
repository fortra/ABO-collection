**Abo-sp.exe**

We run the **Abo** and notice that it is a server that is listening on port 65535

![](media/bcfdda01f9bbc9812512720f91669a76.png)

Observing with Process Hacker, we noticed that it loads a proprietary library called Trapecio.dll

![](media/b63ceea7b00d2b18733a3ce142329b1c.png)

We open the Abo in IDA to see the Main() function

After loading the library, call to **VirtualProtect()** to change the permission of the global variable **buf**, leaving it with **PAGE_READWRITE**, meaning it will not have execution permission.

![](media/c26531d25ea8a0e11b4dc3a8191612cf.png)

Double-clicking on the **buf** variable we notice that it is in the **data** section, which corresponds to a **global variable** and has a size of **256 bytes (0x100).**

![](media/581382b81656f688d538f283c501ed59.png)

Since this is a server that will receive data via socket, let's look at the **recv()** function to see if we can figure out what's going on.

![Interfaz de usuario gráfica, Aplicación Descripción generada automáticamente](media/0291cb568d330513f59a903be97baea8.png)

We can see that it receives the data in the **buf** variable, then it will return in EAX the number of bytes read and it will save that in the variable that it renamed to bytes_leidos

We look for references to know from where the recv function is called and we see that it does so from 2 different places.

![Texto Descripción generada automáticamente](media/a5fc90a05901ec9058c8924f1bcc27a9.png)

The function is called from 2 different places, let's see the first one

comes from this block that starts by doing **memset** to fill the buffer (buf) with 0

![Imagen que contiene Tabla Descripción generada automáticamente](media/a109e5d8ebd420e2300ccd58cbaa501a.png)

There is something striking here, because the buffer has a size of 256, however when calling memset to initialize the buffer with 0, it uses 260 as size, (0x104) that is, 4 more.

![Diagrama Descripción generada automáticamente con confianza baja](media/508b5ae82426d32a1355716e2776ab29.png)

This buffer is where the data that we send by socket will be received, in this case I have sent all “A”

![Tabla Descripción generada automáticamente](media/cb103f66daf96f0532082dc4de2cff1e.png)

Next, a pointer to the **printf()** function is stored next to the 256-byte buffer. All of this happens before calling the **recv()**

![](media/bfd82ceb82d18ae7e74dafb4627e2e50.png)

Since the **recv()** function receives 0x104 bytes (260), we can overwrite the next dword of the **buf** variable which had a size of 0x100 (256), this dword originally contained the pointer to **printf()**

![Texto Descripción generada automáticamente con confianza media](media/82f7b4d21228bac9a74101fb9d61e83b.png)

We can control those 4 bytes by placing an address that contains a **CALL EAX**, but that memory area does not have execution permission since it was changed at the beginning.

The conventional solution would be to do ROP, we have the Trapecio.dll library where we can search for gadgets, but there is a simpler solution. We can try to copy the contents of the **buf** variable to some other memory area that already has execution permissions, for this we would use the **memcpy()** function at 0x402458

![](media/c184f91f5d626ae56f5d716897a3df2d.png)

This function has 3 parameters: Destination, source and number of bytes to copy.

![Interfaz de usuario gráfica, Texto, Aplicación Descripción generada automáticamente](media/685d1a111805ae9c7c56d6c5ba5065d6.png)

We must leave the stack prepared with the arguments to execute the CALL EAX that will end up executing memcpy, with the address of the buf where our data is, which will be the source, and we can use 0x40a115 as the destination. We also have 0x104, which would be the number of bytes to copy.

![Interfaz de usuario gráfica, Texto, Aplicación, Chat o mensaje de texto Descripción generada automáticamente](media/e9acd6516836ccc9a047427c7bb356a3.png)

We will send all this data in the first packet and then we will have to send a second packet to execute our shellcode, for this the CALL EAX must contain the destination address where we copy our data sent in the first packet.

![Interfaz de usuario gráfica Descripción generada automáticamente con confianza media](media/590d3a99bd3efe34584d7cf4eaa88a69.png)

The script:

![A screenshot of a computer program Description automatically generated](media/1f358b03182c8248d76a200ccaffd78a.png)
