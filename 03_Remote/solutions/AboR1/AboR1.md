**AboR1.exe**

We move on to the remote ABO's. (AboR1.exe) We run it from the cmd and we can see the following:

![](media/3b573e172dfeeea15ecbb5779c8c4673.png)

With the process hacker tool we can see that it is a server that is listening on port **27015**

![](media/7ec98583b9f93e4b4cb1e59861f04b92.png)

The **recv** function is used to receive data sent through a socket.

![](media/fc1b3e1599ee0091465758833878cfa8.png)

Then it will print on the console the number of bytes received and check that they are more than 4

![](media/66cddf3f982d73791721a92cf5a12bd0.png)

The first 4 bytes are compared with **0xCAFECAFE**

![](media/219c1b6367f9d98c1dca7ab3ef7270df.png)

If they are not equal, the program does not continue, so we must send those first 4 bytes to be able to continue, and get the **“valid cookie!”** message.

**![](media/baab018d04edadfcc83f39672a876e58.png)**

The **buffer_data** variable has a size of 128 bytes, and will be the destination buffer where the bytes we send to the server (that receives up to 1024 bytes (**buffer_recv**)) will be copied. Then the **memmove()** function will copy the amount of bytes received into the **buffer_data** variable, thus being able to overflow it and overwrite the return address to control the flow of the program.

![](media/6811abfbae33b75d7246cb82a8d757b0.png)

![](media/c0e4458c24b53adf58cd5d22bf956e4e.png)

We will overwrite the return address with a **JMP ESP**

![](media/63856bb5be49bb578815ee280c4e47fd.png)

La forma que encontré de saltar a la **shellcode** es a traves de un **jmp esp**, la cual lo encontramos aquí:

![](media/b7fbc4863ef35d3011e5dd69f51d807d.png)

And at the end of the **JMP ESP** address we send the shellcode to run the calculator

![A screen shot of a computer Description automatically generated](media/2d8662f3a4ba0d5b677449f60e55cc11.png)

![](media/49be19a5fdef856b98989c58005a9286.png)
