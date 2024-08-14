**ABO4_VS_2017.exe**

In this **abo** we have 2 variables, a **buffer** and a pointer to another **pbuf** buffer that is created with the **malloc** function. The buffer that **pbuf** points to is **0x64 (100) bytes** in size

![](media/2728c63ed5fecf4ca0bda9976ca71b4c.png)

We also see a **global variable fn**, we know it's **global** because it's defined in the **DATA section**

**![](media/a210a2420bcf2d7385ba86030df50904.png)**

The **global variable fn**  is initialized with the **pointer** to the puts function **,** and since it **is not** a local variable then it does not take up space on the **stack.** All accesses to it are not through the stack, but directly from the memory of the **process**.

**![](media/2450407d74a09b17b5f7dba34c0f8e56.png)**

The **buf** variable is going to be filled with the data that we enter by keyboard.

![](media/415c931ed510484141c6b00027ba6038.png)

Then fill the second **buffer** pointed by **pbuf**

![](media/8d60c52d4479be2a1d5604f8bee5ab58.png)

This second buffer was created with **malloc(),** which is a function used to allocate a block of memory in the **heap**. The program accesses this block of memory through a pointer that **malloc** returns in the **EAX** register. When the memory is no longer needed, the pointer is passed to the **free** function, which frees up the memory so that it can be used for other purposes.

Finally, it executes the **fn** function that originally contained the direction of the **puts()** function, and what it does is print the contents of **buf on the screen**

![](media/e80858fc64d653f84616214779a25d22.png)

Now let's look at the arrangement of the variables in the stack

![](media/f70716b7ec2d7b45491107377e8323cc.png)

Note that in the code there is still the **system**  function located at the address **0x402657** this can be useful to us.

**![](media/b433264df9018f3712ae70ff3c9a2795.png)**

So it occurred to me again to do the same thing as in the **ABO3**, that is, to run the calculator with the **system function**

![](media/e069e3a6e8592808bfda0ea1b4e35480.png)

Originally **\_fn** points to the **system function,** just before the address of the **put is assigned.**

**![](media/e115f719e3652ef44f39fbc4462b71a3.png)**

We can check it by double-clicking on **\_fn**

![](media/a23e5e1924eda65886c57e71f47cf05f.png)

Let's look at the **Hex View window**

![](media/bbc2d24238a09e05f22e83f859683754.png)

The content of **0x00415000 (_fn)** is **0x00402657 (system)**

**![](media/b433264df9018f3712ae70ff3c9a2795.png)**

**pbuf**  is used as an **argument** in the **second gets**, so with the **first gets** we could step on the **pbuf** pointer **,** making it point to **0x00415000 (_fn).**

![](media/854527d73cfd31fb20ecf6f875657c2d.png)![](media/7a95a93ef7cfeafbebadfd853b7c6184.png)

Then he uses **pbuf,** which now aims to **\_fn,**  as the argument of the **second gets.**

**![](media/624c9c4af4801cbcf6d23396ebde164d.png)**

So to point to **system**  again we must send it the address **0x00402657 (system)** by keyboard

**![](media/03dc2195aa7b2bcc782c47f98cf6d63e.png)**

In this case, as there are two **gets**, in the **python**  script we have to end in the first one with a carriage return (**"\\n")**

The script:

| import sys import binascii from subprocess import Popen, PIPE  buff = b"calc" + b"\\x00"  pointer_fn = b"\\x00\\x50\\x41\\x00" \# funcion \_fn pointer_system = b"\\x57\\x26\\x40\\x00" \# funcion system pbuff = b"\\x90" \* 4  buffer = buff + b"A" \* (0x100 - len(buff)) buffer += pointer_fn + b"\\n" buffer += pointer_system  payload = buffer  p1 = Popen("ABO4_VS_2017.exe", stdin=PIPE) print ("PID: %s" % hex(p1.pid)) print ("Enter para continuar")  p1.communicate(payload) p1.wait() input() |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

![](media/4a04f01a06496e95514e53bd3f15d6de.png)
