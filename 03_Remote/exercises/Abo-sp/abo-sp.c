/****************************************************************************/

#include <windows.h>
#include "objetos\objetos.h"
#include "objetos\socket.cc"

/****************************************************************************/

typedef struct
{
  unsigned char *address;
  int size;
} command;

void f ( Socket * );
int recv_data ( Socket * , char * , unsigned int , int * );
int chequear_memoria ( unsigned char * , unsigned int , unsigned char * );

/****************************************************************************/

char data [260];

/****************************************************************************/

int main ( void )
{
  Socket *socket;
  Socket *client;
  int oldp;

/* Cargo una lib para GARANTIZAR gadgets donde saltar */
  LoadLibrary ( "trapecio.dll" );

/* Seteo permisos de NO EXECUTE al .DATA */
  VirtualProtect ( ( void * ) data , sizeof ( data ) , PAGE_READWRITE , &oldp );

/* Creo el objeto */
  socket = new ( Socket );

/* Acepto conexiones infinitas */
  while ( 1 )
  {
    printf ( "listening in port %i ...\n" , 65535 );

  /* Espero una conexion */
    client = Socket_Accept ( socket , "65535" );

  /* Si hay una nueva conexion */
    if ( client != NULL )
    {
    /* Mensaje al usuario */
      printf ( "[x] Connection established\n" );

    /* Llamo a la funcion que lee data del socket */
      f ( client );

    /* Cierro el socket */
      Socket_Close ( client );

    /* Mensaje al usuario */
      printf ( "[x] Connection closed\n" );
    }
  }
}

/****************************************************************************/

void f ( Socket *client )
{
  int ( *fn ) ( char * , ... );
  int bytes_leidos;

/* Limpio el buffer */
  memset ( data , 0 , 260 );
  * ( unsigned int * ) &data [ 256 ] = printf;

/* Leo la data del socket */
  Socket_Recv ( client , data , 260 , &bytes_leidos );

/* Imprimo la data recibida */
  ( void * ) fn = * ( unsigned int * ) &data [ 256 ];
  fn ( "data: %s\n" , data );
}

/****************************************************************************/

int recv_data ( Socket *client , char *buffer , unsigned int len , int *bytes_leidos )
{
  unsigned int leidos;
  unsigned int cont;
  unsigned char c;
  int ret = TRUE;

/* Levanto toda la data del socket */
  for ( cont = 0 ; cont < len ; cont ++ )
  {
  /* Leo la data del socket */
    ret = Socket_Recv ( client , ( char * ) &c , 1 , &leidos );

  /* Si la data pudo ser leida */
    if ( ret == TRUE )
    {
    /* Copio la data al buffer de destino */
      buffer [ cont ] = c;
    }
  /* Dejo de leer */
    else
    {
      break;
    }
  }

/* Retorno la cantidad de bytes leidos */
  *bytes_leidos = cont;

  return ( ret );
}

/****************************************************************************/

