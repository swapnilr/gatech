#include <stdlib.h>
#include <string.h>
#include <rpc/rpc.h>
#include <sys/dir.h>

char ** httpget_1_svc(char** url, struct svc_req* req){
  static char *msg = NULL;

  if( msg == NULL)
    msg = (char *) malloc(9);

  strcpy(msg, "SUCCESS!");

  return &msg;
}
