// use-after-free.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <Windows.h>

BYTE data[1024];


class MySuperObject
{
	public:	
//		MySuperObject();
//		~MySuperObject();
		virtual bool Create(char *filename)=0;
		virtual bool Open(char *filename)=0;
		virtual void Write(BYTE *data, DWORD size)=0;
		virtual void Read(BYTE *data, DWORD size)=0;
		virtual void Seek(LONG distance)=0;
		virtual DWORD GetSize()=0;
		virtual void Close()=0;

	protected:
		HANDLE h_file;
		char _filename[MAX_PATH];
};

class FileIO: public MySuperObject
{
	public:	
		FileIO();
		~FileIO();
		virtual bool Create(char *filename);
		virtual bool Open(char *filename);
		virtual void Write(BYTE *data, DWORD size);
		virtual void Read(BYTE *data, DWORD size);
		virtual void Seek(LONG distance);
		virtual  DWORD GetSize();
		virtual void Close();

};

FileIO::FileIO()
{
	h_file = INVALID_HANDLE_VALUE;
}

FileIO::~FileIO()
{

}

bool FileIO::Create(char *filename)
{
	h_file = CreateFile(filename, GENERIC_WRITE | GENERIC_READ, FILE_SHARE_READ, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, 0);
	if(h_file == INVALID_HANDLE_VALUE) {
//		LogLine("ERROR: cannot create %s\r\n", filename);
		return false;
	}
	lstrcpyn(_filename, filename, MAX_PATH);
	return true;
}

bool FileIO::Open(char *filename)
{
	h_file = CreateFile(filename, GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, 0);
	if(h_file == INVALID_HANDLE_VALUE) {
		return false;
	}
	lstrcpyn(_filename, filename, MAX_PATH);
	return true;
}

void FileIO::Write(BYTE *data, DWORD size)
{
	DWORD tmp=0;
	WriteFile(h_file, data, size, &tmp, 0);
	if(tmp != size) {
//		LogLine("ERROR: writting to %s\r\n", _filename);
	}
}

void FileIO::Read(BYTE *data, DWORD size)
{
	DWORD tmp=0;
	ReadFile(h_file, data, size, &tmp, 0);
	if(tmp != size) {
//		LogLine("ERROR: reading to %s\r\n", _filename);
	}
}

void FileIO::Seek(LONG distance)
{
	LONG hi=0; 
	SetFilePointer(h_file, distance, &hi, FILE_BEGIN);
}

DWORD FileIO::GetSize()
{
	if(h_file == INVALID_HANDLE_VALUE) {
//		LogLine("ERROR: file is not open\r\n");
		return(0);
	} 
	
	DWORD tmp=0;
	return GetFileSize(h_file, &tmp);
}

void FileIO::Close()
{
	CloseHandle(h_file);
}


int _tmain(int argc, _TCHAR* argv[])
{

	memset(data, 0xff, sizeof(data));
	FileIO *file = new FileIO;

	file->Create("somefilename.dat");
	file->Write(data, sizeof(data));
	file->Close();

	delete file;

	BYTE *otradata = new BYTE[sizeof(FileIO)];
	gets((char *)otradata );

	file->Close();

	return 0;
}

