// heapoverflow.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <windows.h>

#pragma pack(push, 1)
typedef struct somestruct {
	DWORD size;
	DWORD location;
	DWORD callback;
	DWORD next;
} somestruct;
#pragma pack(pop)


void lanadamisma()
{
	printf(".");
	Sleep(1);
}

int _tmain(int argc, _TCHAR* argv[])
{
	unsigned int arraysize = 10;
	DWORD *dwordarray = new DWORD[arraysize*sizeof(DWORD)];			// same size as somestruct 0xa0
	somestruct *structarray = new somestruct[arraysize];
	for(unsigned int i=0;i<arraysize;i++) {
		structarray[i].size = sizeof(somestruct);
		structarray[i].location = (DWORD)&structarray[i];
		structarray[i].callback = (DWORD)&lanadamisma;
		if(i < (arraysize-1))
			structarray[i].next = (DWORD)&structarray[i+1];
		else
			structarray[i].next = 0;
	}
	gets((char *)dwordarray);


	for(unsigned int i=0;i<arraysize;i++) {
		void (*pFn)(void) = 0;
		pFn = (void (__cdecl *)(void))structarray[i].callback;
		pFn(); 
	}
	delete structarray;

	return 0;
}

