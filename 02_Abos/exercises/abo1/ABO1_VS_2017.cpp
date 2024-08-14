/* abo4-stdin.c                                                    *
* specially crafted to feed your brain by gera@core-sdi.com */

/* After this one, the next is just an Eureka! away          */

#define _CRT_SECURE_NO_WARNINGS
#define _CRT_SECURE_NO_DEPRECATE

#include <stdlib.h>
#include  <stdio.h> 
#include "Windows.h"


void f(int nada) {
	char buf[1024];

	gets(buf);
}

int main(int argc, char **argv) {
	MessageBoxA((HWND)-0, (LPCSTR) "A ejecutar la calculadora..\n", (LPCSTR)"Vamosss", (UINT)0);
	f(1);
	printf("hola\n");
}