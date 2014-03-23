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
  cl = clnt_create(server, HTTPGETPROG, HTTPGETVERS, "tcp");
  if (cl == (CLIENT *)NULL) {
    /*
     * Couldn't establish connection
     * with server.
     * Print error message and die.
     */
    clnt_pcreateerror(server);
    exit(1);
  }
  /*
   * Call the remote procedure
   * "printmessage" on the server
   */
  result = httpget_1(&url, cl);
  if (result == (char **)NULL) {
     /*
      * An error occurred while calling 
      * the server.
      * Print error message and die.
      */
    clnt_perror(cl, server);
    exit(1);
  }
   /* Okay, we successfully called 
    * the remote procedure. 
    */
  if (*result == 0) {
      /*
       * Server was unable to print 
       * our message.
       * Print error message and die.
       */
      fprintf(stderr, "%s: could not print your message\n",argv[0]);
      exit(1);
  }
    /* The message got printed on the
     * server's console
     */
  printf("%s", *result);
  clnt_destroy( cl );
  return 0;
}
