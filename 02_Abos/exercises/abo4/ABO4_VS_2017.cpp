/* abo4-stdin.c                                                    *
* specially crafted to feed your brain by gera@core-sdi.com */

/* After this one, the next is just an Eureka! away          */

#define _CRT_SECURE_NO_WARNINGS
#define _CRT_SECURE_NO_DEPRECATE

#include <stdlib.h>
#include  <stdio.h> 
#include "Windows.h"

void(*fn)(char*) = (void(*)(char*))&system;

int main(int argc, char **argv) {

	MessageBoxA ((HWND)-0,(LPCSTR) "A ejecutar la calculadora..\n",(LPCSTR)"Vamosss",(UINT) 0);

	char *pbuf = (char *) malloc(100);
	char buf[256];


	fn = (void(*)(char*))&puts;
	gets(buf);
	gets(pbuf);
	fn(buf);
	while (1);
}
