**AboR2.exe**

It is the turn of the second level of remote ABO's, in this case **Abor2**

Unlike the previous level, when executed this one does not print any message on the console.

![](media/4d5de9c7bbac7ad34bf6636591d374e2.png)

We use the Process Hacker tool to see which port it is listening on, although we could also do it manually.**![](media/188d25ee13ed21e53aaa27686d96cf53.png)**

This is what the flowchart looks like in **IDA**

![](media/a9d92cf0879a6f51a135a8a393d05594.png)

In this line of code the program will receive the data that we send to the server, using the **recv()** function

![](media/f42b8d963ac48c2b465a0c2b1a7b1412.png)

Then it checks that more than 8 bytes are sent, otherwise it exits

**![](media/e12b448a44c617971d33958937af0d4d.png)**

The first 4 bytes are compared with **0xCAFECAFE![](media/acddd31c943b9a6b1512d2f4cb0ca060.png)**

Then below we have the **memcpy** function that copied the received bytes into the **var_88** buffer

But before copying, it compares that the size (controlled by us and corresponding to the fifth byte sent) is less than 0x64, and if it is greater, avoid the block that makes the memcpy

**![](media/8268ca3b6e3e5fcfa910a4350b215ca3.png)**

![](media/2364520b64eb2ed230c7426826fe0918.png)

Looking at the stack frame I can calculate how many bytes I would need to produce an overflow and override the return address, but in this case overriding the return address is useless since the program has a mitigation (security cookie) that checks the integrity of the return address so that in the event of an overflow, the program closes.

**![](media/b0626c798d70d44b4a207560975a5257.png)**

Also, to overwrite the return address we would need 144 bytes, but the previous comparison with the maximum of 0x64 (100) would prevent this from happening.

**![](media/39a7bbad154577a7a1f9c1eddbc82d3d.png)**

One of the arguments of the **memcpy**() function is a size (**size_t**), that is, an unsigned integer, meaning it is always positive.

| void \*memcpy(void \*dest, const void \* src, size_t n) |
|---------------------------------------------------------|

The trick is in this line:

![](media/4c7bd660ffe7a13841d155d840bd7fe2.png)

The **JG** (jump if greater) is a jump that considers the sign, and since it is a single byte, we would have that from 0 to 0x7F it is positive and from 0x80 to 0xff it is negative, so I can send a byte that is between 0x80 and 0xFF and for the program this value would be less than 0x64 since it is negative.

![](media/638fca02acfe434e65c491b785a1a1d9.png)

Note that the **memcpy** function will take this size as **positive**

Let's try to place a negative value as the fifth byte (anything greater than 0x7f), for example: 0x90, This would pass the comparison with 0x64 without problems and would go to memcpy to copy and overflow the stack.

![A screenshot of a computer Description automatically generated](media/9f64a6a32e815b57071637fdbd6f2d75.png)

![](media/22eaf8b55f791c5f2b95fe475f5c6167.png)

![](media/31cc50ee811b216f177b2a276b2ac026.png)

We have overflowed the entire stack and overwritten the **SHE**

![](media/42d4e5e79d93a36474ffb2f243160c31.png)

Now we just need to calculate the number of bytes needed to overwrite the SEH and overwrite it with some address with the instructions: pop, pop, ret to be able to jump to our shellcode.

![A screen shot of a computer Description automatically generated](media/251ea7c8604fe358a24665c495b41e3a.png)

We need 0xc8 bytes but we have to take into account placing a jump just above so that when jumping to execute we can go over the SEH address. We would have to send 0xc4 + a jump 4 bytes further ahead and then the address of pop, pop, ret (401a5c)

**![A screenshot of a computer Description automatically generated](media/7e88aee60d110f19b7b20947c7a1405b.png)**

![](media/40958e45eda36b6b4d4c43730c4c0657.png)

Then we would have the shellcode to run the calculator and we would also add a call to ExitProcess to end the program and prevent it from recursively returning to the SEH and running multiple calculators.

**![](media/5bed4b9537c7ed92cdb801006499761f.png)**

The script:![A screen shot of a computer The script for ABO R2](media/d070ad00ea23ce2aa6a60b6818109aae.png)

Referencias:

-   <https://www.tutorialspoint.com/c_standard_library/c_function_memcpy.htm>
-   <https://en.cppreference.com/w/c/types/size_t>
-   [JG (signed)](http://unixwiz.net/techtips/x86-jumps.html)
-   [size_t](https://www.informit.com/articles/article.aspx?p=686170&seqNum=6)
-   <https://blog.feabhas.com/2014/10/vulnerabilities-in-c-when-integers-go-bad/>
-   
