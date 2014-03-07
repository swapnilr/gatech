#ifndef INDEXMINPQ_H
#define INDEXMINPQ_H

/* 
* Implementation of an indexed min priority queueu.  Adapted from
* Robert Sedgewich and Kevin Wayne's "Algorithms" text.
* http://algs4.cs.princeton.edu/24pq/IndexMaxPQ.java.html
*/

typedef void* indexminpq_key;

typedef struct{
  int NMAX;
  int N;
  int* pq;
  int* qp;
  indexminpq_key* keys;
  int (*keycmp)(indexminpq_key a, indexminpq_key b);
}indexminpq_t;

void indexminpq_init(indexminpq_t* this, int NMAX, int (*keycmp)(indexminpq_key a, indexminpq_key b));
int indexminpq_isempty(indexminpq_t* this);
int indexminpq_contains(indexminpq_t* this, int i);
int indexminpq_size(indexminpq_t* this);
void indexminpq_insert(indexminpq_t* this, int i, indexminpq_key key);
int indexminpq_minindex(indexminpq_t* this);
indexminpq_key indexminpq_minkey(indexminpq_t* this);
int indexminpq_delmin(indexminpq_t* this);
indexminpq_key indexminpq_keyof(indexminpq_t* this, int i);
void indexminpq_changekey(indexminpq_t* this, int i, indexminpq_key key);
void indexminpq_decreasekey(indexminpq_t *this, int i, indexminpq_key key);
void indexminpq_increasekey(indexminpq_t *this, int i, indexminpq_key key);
void indexminpq_delete(indexminpq_t *this, int i);
void indexminpq_destroy(indexminpq_t* this);

#endif
