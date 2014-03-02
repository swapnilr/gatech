#include <omp.h>
#include "gtmp.h"
#include <stdio.h>

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

typedef enum { false, true } bool;

static int count;
static bool sense;
static int P;

void gtmp_init(int num_threads){
  //printf("INIT\n");
  count = num_threads;
  sense = true;  
  P = num_threads;
}

void gtmp_barrier(){
  bool local_sense = !(sense);
  if(__sync_fetch_and_sub(&count, 1) == 1) {
    //printf("Count %d\n", count);
    count = P;
    sense = local_sense;
  } else {
    while(local_sense != sense) {
      //Just hang out
    }
  }
}

void gtmp_finalize(){

}
