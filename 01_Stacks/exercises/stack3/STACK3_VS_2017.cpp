/* abo4-stdin.c                                                    *
* specially crafted to feed your brain by gera@core-sdi.com */

/* After this one, the next is just an Eureka! away          */

#define _CRT_SECURE_NO_WARNINGS
#define _CRT_SECURE_NO_DEPRECATE

#include <stdlib.h>
#include  <stdio.h> 
#include "Windows.h"


int main(int argc, char **argv) {


	MessageBoxA((HWND)-0, (LPCSTR) "Imprimir You win..\n", (LPCSTR)"Vamosss", (UINT)0);

	int cookie;
	char buf[80];

	printf("buf: %08x cookie: %08x\n", &buf, &cookie);
	gets(buf);

	if (cookie == 0x01020005)
		printf("you win!\n");

}

