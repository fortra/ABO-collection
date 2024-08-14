When you open the **STACK1_VS_2017**.**exe** on **IDA**  the first thing you see is the **Prologue** of the function.

![](media/1d036686a092ef8130f92c5b458ca1c4.png)

Here the old base pointer of some previous routine is pushed**,** and then the new base pointer  of this function is fixed. The memory space that will be needed is reserved, it is **0x54 (84) bytes**.

We know that when entering a function, the return address is pushed **,** so the stack will look like this:

![](media/0cd09290037e3ecd2b03212622b08edc.png)

**EBP** that is now the **new base pointer** is fixed, and will serve to point to the **local variables**, and move through the **stack frame** for whatever is necessary.

**IDA,** when entering a function shows us at the beginning the declaration of variables and the arguments.

![](media/ff834be3a2b06e7bff695c7da1285826.png)

There it shows us the offset in the stack where they will be located, we put this data on a table, and it looks like this:

![](media/809b26ee8308e65b8724077fb9ecf081.png)

The same thing is already done by **IDA** automatically if we double click on any **local variable** it will send us to the stack window.

![](media/85a92cdda75df03921aa5df026122727.png)

On the image below, we can see that the size of the variable **var_54** is **0x50 (80) bytes**, we can convert it into an **array** to see it better

![](media/5d4f1bb8ab3a9f67ffeb5da9ea9fcedf.png)

![](media/ff724e13086ef54aa4e238f434bc05fb.png)

**IDA** automatically calculates the size of this variable, which is **0x80** bytes.

now we can see it better on the stack window

![](media/8229baade524f21594914298604ecd42.png)

Let’s rename **var_54** to **buffer**, and **var_4 we**  will call it **cookie**, to do this we stand on the variable and press the **N key**, or choose **rename** from the menu

which unfolds with a right click.

![](media/d1e4d7bae56139e30ca503978d26d65f.png)

Continuing with the analysis, we see that a **MessageBox** appears that we must accept in order to continue, and then, a message is printed in the console with the addresses of the variables **buffer** and **cookie**.

**![](media/237983c207d180c39abd0f04ebd62b78.png)**

It then pushes a pointer to the beginning of the **buffer** variable  that is passed as an argument to the gets() function**.**

![](media/767485b9af23697a5a99b338d0c36705.png)

Finally it is fixed if the **variable coockie** is equal to 0x41424444, in case it is equal then it will show the message:  **"you win!"**

![](media/3623acc9be2258f01f0839fc847c0baf.png)

Otherwise the program will end up doing nothing.

Very well, let's remember how we had the stack:

![](media/a8241d79e2cf1b0ec583fe0bd5b9cf9e.png)

The **gets**  function does not check the buffer length. We can take advantage of this and overflow  the **buffer** variable to step on the **cookie variable**  with the **0x41424344** value**.**

Then we will send 80 bytes plus the cookie value: 0x41424344.

My python script to exploit this exercise is as follows:

| import sys from subprocess import Popen, PIPE  buffer = b"A" \* 80 cookie = b"\\x44\\x43\\x42\\x41"  payload = buffer + cookie  p1 = Popen("STACK1_VS_2017.exe", stdin=PIPE) print ("PID: %s" % hex(p1.pid)) print ("Enter para continuar")  p1.communicate(payload) p1.wait() input() |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

Once you accept the messagebox you’ll see the **"you win!"** message

**![](media/a6c8e9974e6e37abc7c07c4bc08cfa9c.png)**
