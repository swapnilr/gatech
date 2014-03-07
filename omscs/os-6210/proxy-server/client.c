#include <stdlib.h>
#include <stdio.h>
#include <rpc/rpc.h>
#include "proxy_rpc.h" 

int main(int argc, char* argv[]){
  CLIENT *cl;
  char** result;
  char* url;
  char* server;
  
if (argc < 3) {
    fprintf(stderr, "usage: %s host url\n", argv[0]);
    exit(1);
  }
  /*
   * Save values of command line arguments
   */
  server = argv[1];
  url = argv[2];

  /*
   * Your code here.  Make a remote procedure call to
   * server, calling httpget_1 with the parameter url
   * Consult the RPC Programming Guide.
   */


   

  return 0;
}
