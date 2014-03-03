#include <stdlib.h>
#include <stdio.h>
#include <mpi.h>
#include "gtmpi.h"
/*
    From the MCS Paper: The scalable, distributed dissemination barrier with only local spinning.

    type flags = record
        myflags : array [0..1] of array [0..LogP - 1] of Boolean
	partnerflags : array [0..1] of array [0..LogP - 1] of ^Boolean
	
    processor private parity : integer := 0
    processor private sense : Boolean := true
    processor private localflags : ^flags

    shared allnodes : array [0..P-1] of flags
        //allnodes[i] is allocated in shared memory
	//locally accessible to processor i

    //on processor i, localflags points to allnodes[i]
    //initially allnodes[i].myflags[r][k] is false for all i, r, k
    //if j = (i+2^k) mod P, then for r = 0 , 1:
    //    allnodes[i].partnerflags[r][k] points to allnodes[j].myflags[r][k]

    procedure dissemination_barrier
        for instance : integer :0 to LogP-1
	    localflags^.partnerflags[parity][instance]^ := sense
	    repeat until localflags^.myflags[parity][instance] = sense
	if parity = 1
	    sense := not sense
	parity := 1 - parity
*/

static int P;

int pow(base, exponent) {
  int power = 1;
  while(exponent > 0) {
    power = power * base;
    exponent = exponent - 1;
  }
  return power;
}

int log(int v) {
  int r = 0; // r will be lg(v)
  while (v >>= 1) // unroll for more speed...
  {
    r++;
  }
  return r;
}

int ceil_log(int ans) {
  int lg = log(ans);
  if(pow(2, lg) < ans) {
    return lg + 1;
  }
  return lg;
}

void gtmpi_init(int num_threads){
  P = num_threads;
}

void gtmpi_barrier(){
  int vpid, i;

  MPI_Comm_rank(MPI_COMM_WORLD, &vpid);

  int rounds = ceil_log(P);

  for(i=0; i<rounds; i++) {
    int dest = (vpid + pow(2,i)) % P;
    //printf("dest = %d, coming from source = %d, %d\n", dest, vpid, P);
    MPI_Send(NULL, 0, MPI_INT, dest, 1, MPI_COMM_WORLD);
    MPI_Status temp;
    int source = vpid - pow(2,i);
    while(source < 0) {
      source = (source + P) % P;
    }
    MPI_Recv(NULL, 0, MPI_INT, source, 1, MPI_COMM_WORLD, &temp);
  }
  
}

void gtmpi_finalize(){

}
