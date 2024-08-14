
/* ABO - Integer Overflow ( Chup-It ! ) */

void main ( int argc , char *argv [] )
{ 
  char buffer [ 256 ];
  unsigned int bytes_to_copy;
  unsigned int offset;

/* Checking parameters */
  if ( argc != 3 )
  {
    printf ( "y los parametros ?\n" );
    return;
  }

/* Getting string offset */
  sscanf ( argv [ 1 ] , "%u" , &offset );

/* Checking string limit */
  if ( buffer + offset * 4 + strlen ( argv [ 2 ] ) > buffer + sizeof ( buffer ) - 1 )
  {
    printf ( "no no\n" );
    return;
  }

/* Copying string */
  strcpy ( buffer + offset * 4 , argv [ 2 ] , sizeof ( buffer ) );

/* Printing message */
  printf ( "%s\n" , buffer + offset * 4 );
}