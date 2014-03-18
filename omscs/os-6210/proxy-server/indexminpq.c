#include <stdlib.h>
#include <stdio.h>
#include "indexminpq.h"

static int greater(indexminpq_t* this, int i, int j){
  return this->keycmp(this->keys[this->pq[i]],this->keys[this->pq[j]]) > 0;
}

static void exch(indexminpq_t* this, int i, int j){
  int swap;
  swap = this->pq[i]; 
  this->pq[i] = this->pq[j]; 
  this->pq[j] = swap;
  
  this->qp[this->pq[i]] = i; 
  this->qp[this->pq[j]] = j;
}

static void swim(indexminpq_t* this, int k)  {
  while (k > 1 && greater(this, k/2, k)) {
    exch(this, k, k/2);
    k = k/2;
  }
}

static void sink(indexminpq_t* this, int k) {
  int j;
  while (2*k <= this->N) {
    j = 2*k;
    if (j < this->N && greater(this, j, j+1)) j++;
    if (!greater(this, k, j)) break;
    exch(this, k, j);
    k = j;
  }
}


void indexminpq_init(indexminpq_t* this, int NMAX, int (*keycmp)(indexminpq_key a, indexminpq_key b)){
  int i;

  this->NMAX = NMAX;
  this->N = 0;
  this->pq = (int*) malloc(sizeof(int) * (NMAX + 1));
  this->qp = (int*) malloc(sizeof(int) * (NMAX + 1));
  this->keys = (indexminpq_key*) malloc(sizeof(indexminpq_key) * (NMAX + 1));
  this->keycmp = keycmp;

  for(i = 0; i <= NMAX; i++)
    this->qp[i] = -1;
}

int indexminpq_isempty(indexminpq_t* this){ 
  return this->N == 0; 
}

int indexminpq_contains(indexminpq_t* this, int i) {
  if (i < 0 || i >= this->NMAX){
    fprintf(stderr, "Error: Argument to indexminpq_contains out of bounds\n");
    fflush(stderr);
    exit(EXIT_FAILURE);
  }
  return this->qp[i] != -1;
}

int indexminpq_size(indexminpq_t* this) {
  return this->N;
}

void indexminpq_insert(indexminpq_t* this, int i, indexminpq_key key) {
  if (i < 0 || i >= this->NMAX){
    fprintf(stderr, "Error: Argument to indexminpq_contains out of bounds\n");
    fflush(stderr);
    exit(EXIT_FAILURE);
  }
  
  if (indexminpq_contains(this, i)){
    fprintf(stderr, "Error: index %d is already in the indexminpq structure.", i);
    fflush(stderr);
    exit(EXIT_FAILURE);
  }
   
   this->N++;
   this->qp[i] = this->N;
   this->pq[this->N] = i;
   this->keys[i] = key;
   swim(this, this->N);
}

int indexminpq_minindex(indexminpq_t* this) { 
  if (this->N == 0){
    fprintf(stderr, "Error: underflow in indexminpq_minindex.");
    fflush(stderr);
    exit(EXIT_FAILURE);
  }
  return this->pq[1];        
}

indexminpq_key indexminpq_minkey(indexminpq_t* this) { 
  if (this->N == 0){
    fprintf(stderr, "Error: underflow in indexminpq_minkey.");
    fflush(stderr);
    exit(EXIT_FAILURE);
  }
  return this->keys[this->pq[1]];        
}

int indexminpq_delmin(indexminpq_t* this) { 
  int min;
  
  if(this->N == 0){
    fprintf(stderr, "Error: underflow in indexminpq_delmin.");
    fflush(stderr);
    exit(EXIT_FAILURE);
  }
  
  min = this->pq[1];        
  exch(this, 1, this->N); 
  this->N--;
  sink(this, 1);
  this->qp[min] = -1;  /* marking as deleted */
  return min; 
}

indexminpq_key indexminpq_keyof(indexminpq_t* this, int i) {
  if (i < 0 || i >= this->NMAX){
    fprintf(stderr, "Error: Argument to indexminpq_keyof out of bounds\n");
    fflush(stderr);
    exit(EXIT_FAILURE);
  }

  if (!indexminpq_contains(this, i)){
    fprintf(stderr, 
	    "Invalid argument to indexminpq_keyof: index %d is not in the priority queue", i);
    fflush(stderr);exit(EXIT_FAILURE);
  }
  return this->keys[i];
}

void indexminpq_changekey(indexminpq_t* this, int i, indexminpq_key key) {
  if (i < 0 || i >= this->NMAX){
    fprintf(stderr, "Error: Argument to indexminpq_changekey out of bounds\n");
    fflush(stderr);
    exit(EXIT_FAILURE);
  }
  
  if (!indexminpq_contains(this, i)){
    fprintf(stderr,
	    "Invalid argument to indexminpq_changekey: index %d is not in the priority queue", i);
    fflush(stderr);
    exit(EXIT_FAILURE);  
  }
  this->keys[i] = key;
  swim(this, this->qp[i]);
  sink(this, this->qp[i]);
}

void indexminpq_decreasekey(indexminpq_t *this, int i, indexminpq_key key) {
  if (i < 0 || i >= this->NMAX){
    fprintf(stderr, "Error: Argument to indexminpq_decreasekey out of bounds\n");
    fflush(stderr);
    exit(EXIT_FAILURE);
  }

  if (!indexminpq_contains(this, i)){
    fprintf(stderr,
	    "Invalid argument to indexminpq_decreasekey: index %d is not in the priority queue", i);
    fflush(stderr);
    exit(EXIT_FAILURE);  
  }
 
  if (this->keycmp(this->keys[i], key) > 0){
    fprintf(stderr,"Error: indexminpq_decreasekey called with increasing key");
    fflush(stderr);
    exit(EXIT_FAILURE);
  }
    
  this->keys[i] = key;
  swim(this, this->qp[i]);
}

void indexminpq_increasekey(indexminpq_t *this, int i, indexminpq_key key) {
  if (i < 0 || i >= this->NMAX){
    fprintf(stderr, "Error: Argument to indexminpq_increasekey out of bounds\n");
    fflush(stderr);
    exit(EXIT_FAILURE);
  }

  if (!indexminpq_contains(this, i)){
    fprintf(stderr,
	    "Invalid argument to indexminpq_increasekey: index %d is not in the priority queue\n", i);
    fflush(stderr);
    exit(EXIT_FAILURE);  
  }
  
  if (this->keycmp(this->keys[i], key) < 0){
    fprintf(stderr,"Error: indexminpq_increasekey called with decreasing key\n");
    fflush(stderr);
    exit(EXIT_FAILURE);
  }

  this->keys[i] = key;
  sink(this, this->qp[i]);
}

void indexminpq_delete(indexminpq_t *this, int i) {
  int index;
  
  if (i < 0 || i >= this->NMAX){
    fprintf(stderr, "Error: Argument to indexminpq_increasekey out of bounds\n");
    fflush(stderr);
    exit(EXIT_FAILURE);
  }
  
  if (!indexminpq_contains(this, i)){
    fprintf(stderr,"Error: Invalid argument to indexminpq_delete: index %d is not in the priority queue", i);
    fflush(stderr);
    exit(EXIT_FAILURE);  
  }

  index = this->qp[i];
  exch(this, index, this->N);
  this->N--;
  swim(this, index);
  sink(this, index);
  this->qp[i] = -1;
}

void indexminpq_destroy(indexminpq_t* this){
  free(this->pq);
  free(this->qp);
  free(this->keys);
}
