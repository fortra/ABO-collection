## Abo Use after free (abo-useafterfree.exe)

Let's reverse engineer this Abo to fully understand where the vulnerability is and how to exploit it.

For this we open it in IDA and begin to analyze the code and rename the variables as we identify them, and putting all the data that we discover.

In the **main()** function we can see that it will fill a buffer with the byte 0xff and then through new it creates an object, this new function is the equivalent of malloc, that is, it will reserve a space in memory of 0x10c for its object.

![A screen shot of a computer Description automatically generated](media/a69af79728ea60134aa74e572acd3687.png)

The variable **unk_411d20** is a global variable since it is located in the .DATA section

![](media/b1c9d27e098c34311a2ec1065a11d19a.png)

we are going to rename it to: buffer

![](media/17e53e7d9c8a07624f7206150479fe4c.png)

Now we are going to create a structure of 0x10C that will be the one that corresponds to the object that is created using the operator new(uint) function and we will complete it as we move forward and see what each field is. For now we will call it **struct_1**

![A screenshot of a computer Description automatically generated](media/3467202e9ce562fc4dc01685d7f6d3f7.png)

And we will name the variable **block** as **myobject** since it will store the address returned by the **NEW** function, which is where the object is located. After creating the object with **new**, simply verifies that the function was successful, and if so, it continues at **text:0x4080Df**.

![A screenshot of a computer program Description automatically generated](media/18dc27b36202cbd2a1d5675018b4079d.png)

By entering the **sub_4083A0** function, we see that it is the constructor of **FileIO**

Here I already have the function reversed, and we can see when it writes the pointer to the **vtable** in the first field of the **struct_1** structure, which we now know its correct name and can rename it and we will also change the type:

![A screen shot of a computer Description automatically generated](media/b7b238c1b12963796d552ca0ad7a7af6.png)

Now, by double-clicking on **vftable**, we will view the **vtable** and assign temporary names to the functions to identify them until we determine their real names. This is the **vtable** with the addresses of the corresponding functions:

![A screen shot of a computer](media/3ec8dca2e4932a8e513867d915e9f673.png)

We'll replace the addresses with names, like this:

![A screen shot of a computer Description automatically generated](media/8c70a01995b5c99cd19dbb33b63cbea5.png)

Now we will create a structure for the **vtable**, select from the beginning to the end, right click create structure from selection

![A screen shot of a computer Description automatically generated](media/d364889111e76c43ce1f5d7ae65f0d24.png)

The structure is created:

![A screen shot of a computer code Description automatically generated](media/544ea3fe8c70b39baa76d89af12d235c.png)

So far then we have created a structure (**struct_1**) for the **FileIO** object and then another structure for the **vtable** of this object that will occupy the first field of struct_1

Now we are going to put names to the things we discovered.

**struct_40E458** to **FileIO_vtable**:

![A screen shot of a computer program Description automatically generated](media/7d76dde67dc575d619a0dff6936dad69.png)

Now let's go to the structure of the object and change the type of the first field that corresponds to the pointer to the vtable, first rename it to **p_vtable** and then change the type:

![A screenshot of a computer program Description automatically generated](media/abefb1a55f073bdf3916a65e91a37811.png)

![A screen shot of a computer Description automatically generated](media/5104a726c20c6f2c453adcafcd35e95a.png)

In this way I am indicating that in **field 0** of my object (FileIO) there will be a pointer to another structure that corresponds to the **vtable**

We've already reversed until after the constructor, we've created and renamed the structures, then we have the following code:

![A screenshot of a computer program Description automatically generated](media/77e923d0adb82ae793872082018b8868.png)

The first thing I notice is that **my_object** starts storing it in different variables, so I'll start renaming what I can identify:

![A computer screen shot of a program code Description automatically generated](media/ae1de4da03cdaac87d6dd4f20a4fdaf1.png)

Now let's select the structures by pressing **T** in the places where it will be used, and the code looks like this:

![A screen shot of a computer code Description automatically generated](media/8ae22d0a83ebd5cabcffeb6bb2af24b6.png)

Let’s see where **vtable.func1** will take us by double-clicking:

![A screenshot of a computer program Description automatically generated](media/ad5c6f934b69a0ac2f6ad4b93618e0e5.png)

First it calls CreateFileA and then lstrcpynA, we can name it: **Create** since it will create a file named **somefile.dat** (the string that passes it as an argument.)

![A screenshot of a computer program Description automatically generated](media/795fdb1483acc66cdcfc1411a683287c.png)

We can improve the **Call edx** a little so that it replaces the name of the register with that of the function we have discovered, we stand on the EDX CALL and press **Alt+F11** and we put the name of the function, in this way if we look for references of it, IDA now knows where it is called from.

![A screenshot of a computer screen Description automatically generated](media/0f3b2e34c74a47ca2a83cead6012403c.png) ![](media/acfad233251df5523f705e9e10ca8080.png)

![A screenshot of a computer Description automatically generated](media/75eb2f6eb2452ffb05e0747bed4937e5.png)

We repeat these steps until the end of the block, it’ll look like this:

![A screenshot of a computer program Description automatically generated](media/d9dd8d84bbcde1e25b3b91b977aa709f.png)

This way everything is much clearer, after calling the vtable functions (Create, Write and Close) it ends up calling **free()** to release the object.

In the next block it creates a new object of the same size, so the system instead of reserving a new space in memory will assign the same address that it has just released by **free(),** and then the program calls the **\_gets()** function whose argument is a buffer where it will store data that we control and ends up calling a function of the **vtable** that we can obviously manipulate.

![A screen shot of a computer Description automatically generated](media/d2c64341dabf48453d82b47c2fd29f29.png)

The script

![A black background with colorful lines Description automatically generated with medium confidence](media/646dd958ee424e22c601c61e4cef959e.png)
