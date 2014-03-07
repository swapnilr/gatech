#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "indexrndq.h"

void indexrndq_init(indexrndq_t* this, int NMAX){
  int i;
  
  this->NMAX = NMAX;
  this->N = 0;
  this->pi = (int*) malloc(sizeof(int) * NMAX);
  this->ip = (int*) malloc(sizeof(int) * NMAX);

  for(i = 0; i < NMAX; i++)
    this->ip[i] = -1;
}

int indexrndq_isempty(indexrndq_t* this){
  return this->N == 0;
}

void indexrndq_enqueue(indexrndq_t* this, int i){
  if (i < 0 || i >= this->NMAX){
    fprintf(stderr, "Error: Argument to indexrndq_enqueue out of bounds\n");
    fflush(stderr);
    exit(EXIT_FAILURE);
  }
  
  if (indexrndq_contains(this, i)){
    fprintf(stderr, "Error: index %d is already in the indexrndq structure.", i);
    fflush(stderr);
    exit(EXIT_FAILURE);
  }

  this->ip[i] = this->N;
  this->pi[this->N] = i;
  this->N++;

  return;
}

int indexrndq_contains(indexrndq_t* this, int i){
  return this->ip[i] != -1;
}

void indexrndq_delete(indexrndq_t* this, int i){
   if (i < 0 || i >= this->NMAX){
    fprintf(stderr, "Error: Argument to indexrndq_contains out of bounds\n");
    fflush(stderr);
    exit(EXIT_FAILURE);
  }
  
  if (!indexrndq_contains(this, i)){
    fprintf(stderr, "Error: index %d is not in the indexrndq structure.", i);
    fflush(stderr);
    exit(EXIT_FAILURE);
  }
  
  this->N--;
  this->pi[this->ip[i]] = this->pi[this->N];
  this->ip[this->pi[this->N]] = this->ip[i];
  this->ip[i] = -1;
}

int indexrndq_dequeue(indexrndq_t* this){
  int ans, k;

  /* Testing for underflow */
  if(this->N <= 0){
    fprintf(stderr, "Error: indexrndq underflow\n");
    fflush(stderr);
    exit(EXIT_FAILURE);
  }

  k = (int) (1.0 * this->N * rand() / (RAND_MAX + 1.0));
  ans = this->pi[k];

  --this->N;

  this->pi[k] = this->pi[this->N];
  this->ip[this->pi[k]] = k;
  this->ip[ans] = -1;

  return ans;
}

void indexrndq_destroy(indexrndq_t* this){
  free(this->pi);
  free(this->ip);
}
