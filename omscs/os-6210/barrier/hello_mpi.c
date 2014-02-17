#include <stdio.h>
#include <sys/utsname.h>
#include "mpi.h"


int main(int argc, char **argv)
{
  int my_id, num_processes;
  struct utsname ugnm;
    
  MPI_Init(&argc, &argv);

  MPI_Comm_size(MPI_COMM_WORLD, &num_processes);
  MPI_Comm_rank(MPI_COMM_WORLD, &my_id);

  uname(&ugnm);

  printf("Hello World from thread %d of %d, running on %s.\n", my_id, num_processes, ugnm.nodename);

  MPI_Finalize();
  return 0;
}

