#include <stdio.h>
#include <sys/utsname.h>
#include "mpi.h"
#include "gtmpi.h"

int main(int argc, char **argv)
{
  int my_id, num_processes;
  struct utsname ugnm;
  
  gtmpi_init(10);
  
  MPI_Init(&argc, &argv);

  MPI_Comm_size(MPI_COMM_WORLD, &num_processes);
  MPI_Comm_rank(MPI_COMM_WORLD, &my_id);

  uname(&ugnm);

  printf("Hello World from thread %d of %d, running on %s.\n", my_id, num_processes, ugnm.nodename);

  //MPI_Barrier(MPI_COMM_WORLD);

  gtmpi_barrier();
  printf("After barrier 1 by %d \n", my_id);

  gtmpi_barrier();
  //MPI_Barrier(MPI_COMM_WORLD);

  printf("HEY LOOK IT WORKED! After barrier 2 by %d \n", my_id);

  gtmpi_finalize();
  MPI_Finalize();
  return 0;
}

