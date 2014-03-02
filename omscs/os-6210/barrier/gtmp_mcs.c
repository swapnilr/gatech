#include <stdlib.h>
#include <stdio.h>
#include <omp.h>
#include "gtmp.h"

/*
    From the MCS Paper: A scalable, distributed tree-based barrier with only local spinning.

    type treenode = record
        parentsense : Boolean
	parentpointer : ^Boolean
	childpointers : array [0..1] of ^Boolean
	havechild : array [0..3] of Boolean
	childnotready : array [0..3] of Boolean
	dummy : Boolean //pseudo-data

    shared nodes : array [0..P-1] of treenode
        // nodes[vpid] is allocated in shared memory
        // locally accessible to processor vpid
    processor private vpid : integer // a unique virtual processor index
    processor private sense : Boolean

    // on processor i, sense is initially true
    // in nodes[i]:
    //    havechild[j] = true if 4 * i+j < P; otherwise false
    //    parentpointer = &nodes[floor((i-1)/4].childnotready[(i-1) mod 4],
    //        or dummy if i = 0
    //    childpointers[0] = &nodes[2*i+1].parentsense, or &dummy if 2*i+1 >= P
    //    childpointers[1] = &nodes[2*i+1].parentsense, or &dummy if 2*i+2 >= P
    //    initially childnotready = havechild and parentsense = false
	
    procedure tree_barrier
        with nodes[vpid] do
	    repeat until childnotready = {false, false, false, false}
	    childnotready := havechild //prepare for next barrier
	    parentpointer^ := false //let parent know I'm ready
	    // if not root, wait until my parent signals wakeup
	    if vpid != 0
	        repeat until parentsense = sense
	    // signal children in wakeup tree
	    childpointers[0]^ := sense
	    childpointers[1]^ := sense
	    sense := not sense
*/

typedef enum { false, true } bool;

typedef struct treenode {
  bool parentsense;
  bool *parentpointer;
  bool *childpointers[2];
  bool havechild[4];
  bool childnotready[4];
  bool dummy;
} treenode;

static treenode *nodes;
static bool *senses;
static int P;

void printitall() {
  int i;
  for(i=0; i<2; i++) {
    printf("NODE %d\n", i);
    printf("Havechild: ");
    int j;
    for(j=0; j<4; j++) {
      printf("%d ", nodes[i].havechild[j]);
    }
    printf("\n");
    printf("Childnotready: ");
    for(j=0; j<4; j++){
      printf("%d ", nodes[i].childnotready[j]);
    }
    printf("\n");
  }
}

void gtmp_init(int num_threads){
  P = num_threads;
  nodes = (treenode *) malloc(sizeof(treenode) * num_threads);
  senses = (bool *) malloc(sizeof(bool) * num_threads);
  int i;
  for(i=0; i<num_threads; i++){
    nodes[i].parentsense = false;
    int j;
    for(j=0; j<4; j++){
      if(((4*i) + j) < num_threads - 1) {
        nodes[i].havechild[j] = true;
      } else {
        nodes[i].havechild[j] = false;
      }
    }
    for(j=0; j<4; j++){
      nodes[i].childnotready[j] = nodes[i].havechild[j];
    }
    if(i==0) {
      nodes[i].parentpointer = &(nodes[i].dummy);
    } else {
      nodes[i].parentpointer = &(nodes[(int)((i-1)/4)].childnotready[(i-1) % 4]);
    }
    if(2*i + 1 >= num_threads) {
      nodes[i].childpointers[0] = &(nodes[i].dummy);
    } else {
      nodes[i].childpointers[0] = &(nodes[2*i + 1].parentsense);
    }
    if(2*i + 2 >= num_threads) {
      nodes[i].childpointers[1] = &(nodes[i].dummy);
    } else {
      nodes[i].childpointers[1] = &(nodes[2*i + 2].parentsense);
    }
  }
  for(i=0; i<num_threads; i++){
    senses[i] = true;
  }
  //printitall();
}

void gtmp_barrier(){
  int vpid = omp_get_thread_num();
  while(nodes[vpid].childnotready[0] || nodes[vpid].childnotready[1] ||
     nodes[vpid].childnotready[2] || nodes[vpid].childnotready[3]) {
    // Gotta wait yo
  }
  //printf("Thread %d done waiting for children\n", vpid);
  int j;
  for(j=0; j<4; j++){
    nodes[vpid].childnotready[j] = nodes[vpid].havechild[j];
  }
  *(nodes[vpid].parentpointer) = false;
  if(vpid != 0) {
    while(senses[vpid] != nodes[vpid].parentsense) {
      // Just hanging out
    }
  }
  *(nodes[vpid].childpointers[0]) = senses[vpid];
  *(nodes[vpid].childpointers[1]) = senses[vpid];
  senses[vpid] = !(senses[vpid]);
  //printitall();
}

void gtmp_finalize(){
  free(nodes);
  free(senses);
}
