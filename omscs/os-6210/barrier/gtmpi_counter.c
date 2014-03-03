#include <stdlib.h>
#include <mpi.h>
#include <stdio.h>
#include "gtmpi.h"

/*
    From the MCS Paper: A sense-reversing centralized barrier

    shared count : integer := P
    shared sense : Boolean := true
    processor private local_sense : Boolean := true

    procedure central_barrier
        local_sense := not local_sense // each processor toggles its own sense
	if fetch_and_decrement (&count) = 1
	    count := P
	    sense := local_sense // last processor toggles global sense
        else
           repeat until sense = local_sense
*/


static int P;

void gtmpi_init(int num_threads){
  P = num_threads;
}


/*
 * The logic is quite simple. While initially every single processor was notifying every other processor,
   instead we leave the counting to one "master" processor, processor 0. So every other processor first sends a message to processor 0.
   Then processor 0 notifies every other processor that the barrier is complete.
 */
void gtmpi_barrier(){
  int vpid, i;

  MPI_Comm_rank(MPI_COMM_WORLD, &vpid);
  MPI_Status temp;
  if(vpid != 0) {
    MPI_Send(NULL, 0, MPI_INT, 0, 1, MPI_COMM_WORLD);
    MPI_Recv(NULL, 0, MPI_INT, 0, 1, MPI_COMM_WORLD, &temp);
  } else {
    for(i=1; i<P; i++) {
      MPI_Recv(NULL, 0, MPI_INT, i, 1, MPI_COMM_WORLD, &temp);
    }
    for(i=1; i<P; i++) {
      MPI_Send(NULL, 0, MPI_INT, i, 1, MPI_COMM_WORLD);
    }
  }
}

void gtmpi_finalize(){
}

