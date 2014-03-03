#include <stdlib.h>
#include <stdio.h>
#include <mpi.h>
#include "gtmpi.h"

/*
    From the MCS Paper: A scalable, distributed tournament barrier with only local spinning

    type round_t = record
        role : (winner, loser, bye, champion, dropout)
	opponent : ^Boolean
	flag : Boolean
    shared rounds : array [0..P-1][0..LogP] of round_t
        // row vpid of rounds is allocated in shared memory
	// locally accessible to processor vpid

    processor private sense : Boolean := true
    processor private vpid : integer // a unique virtual processor index

    //initially
    //    rounds[i][k].flag = false for all i,k
    //rounds[i][k].role = 
    //    winner if k > 0, i mod 2^k = 0, i + 2^(k-1) < P , and 2^k < P
    //    bye if k > 0, i mode 2^k = 0, and i + 2^(k-1) >= P
    //    loser if k > 0 and i mode 2^k = 2^(k-1)
    //    champion if k > 0, i = 0, and 2^k >= P
    //    dropout if k = 0
    //    unused otherwise; value immaterial
    //rounds[i][k].opponent points to 
    //    round[i-2^(k-1)][k].flag if rounds[i][k].role = loser
    //    round[i+2^(k-1)][k].flag if rounds[i][k].role = winner or champion
    //    unused otherwise; value immaterial
    procedure tournament_barrier
        round : integer := 1
	loop   //arrival
	    case rounds[vpid][round].role of
	        loser:
	            rounds[vpid][round].opponent^ :=  sense
		    repeat until rounds[vpid][round].flag = sense
		    exit loop
   	        winner:
	            repeat until rounds[vpid][round].flag = sense
		bye:  //do nothing
		champion:
	            repeat until rounds[vpid][round].flag = sense
		    rounds[vpid][round].opponent^ := sense
		    exit loop
		dropout: // impossible
	    round := round + 1
	loop  // wakeup
	    round := round - 1
	    case rounds[vpid][round].role of
	        loser: // impossible
		winner:
		    rounds[vpid[round].opponent^ := sense
		bye: // do nothing
		champion: // impossible
		dropout:
		    exit loop
	sense := not sense
*/

static int P;

int pow(int base, int exponent) {
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

/*
  if 1,3,5,7... -> 1 round
  if 2,6,10,12... -> 2 rounds
  if 4,8,16... -> 3 rounds
  up to a max of ceil(log(vpid))
*/
int getRounds(int vpid) {
  int max_rounds = ceil_log(P);
  int rounds; 
  for(rounds=1; rounds <= max_rounds; rounds++) {
    if(vpid % pow(2, rounds) != 0){
      return rounds;
    }
  }
  return max_rounds;
}

void gtmpi_init(int num_threads){
 P = num_threads;  
}

void runRound(int vpid, int rounds, int currentRound) {
  if(currentRound == ceil_log(P)) {
    return;
  }
  //int currentRound = ceil_log(P) - rounds;
  //Pick role - winner or loser
  MPI_Status temp;
  if(vpid % pow(2, currentRound + 1) == 0) {
   // Lucky you
    //printf("DEBUG: WINNER: Processor %d is the winner of round %d\n", vpid, currentRound);
    int peer = vpid + pow(2, currentRound);
    if(peer < P) {
      //printf("DEBUG: WINNER: Processor %d waiting for message from %d\n", vpid, peer);
      MPI_Recv(NULL, 0, MPI_INT, peer, 1, MPI_COMM_WORLD, &temp);
      //printf("DEBUG: WINNER: Processor %d got the message from %d\n", vpid, peer);
   }
   runRound(vpid, rounds, currentRound + 1);
   if(peer < P) {
      MPI_Send(NULL, 0, MPI_INT, peer, 1, MPI_COMM_WORLD);
   }
  } else {
    // You lost! First send a message and then wait for receipt
    int peer = vpid - pow(2, currentRound);
    //printf("DEBUG: LOSER: Sending message from %d to %d in round %d\n", vpid, peer, currentRound);
    if(peer >= 0) {
      MPI_Send(NULL, 0, MPI_INT, peer, 1, MPI_COMM_WORLD);
      MPI_Recv(NULL, 0, MPI_INT, peer, 1, MPI_COMM_WORLD, &temp);
    }
  }
}

void gtmpi_barrier(){
  int vpid;

  MPI_Comm_rank(MPI_COMM_WORLD, &vpid);

  // Determine number of rounds for this process
  int rounds = getRounds(vpid);
  //printf("DEBUG: Running %d rounds for %d\n", rounds, vpid);
  runRound(vpid, rounds, 0);
}

void gtmpi_finalize(){

}
