#ifndef INDEXRNDQ_H
#define INDEXRNDQ_H

typedef struct{
  int NMAX;
  int N;
  int* pi;
  int* ip;
}indexrndq_t;

void indexrndq_init(indexrndq_t* q, int NMAX);
int indexrndq_isempty(indexrndq_t* q);
int indexrndq_contains(indexrndq_t* this, int i);
void indexrndq_delete(indexrndq_t* q, int i);
void indexrndq_enqueue(indexrndq_t* q, int i);
int indexrndq_dequeue(indexrndq_t* q);
void indexrndq_destroy(indexrndq_t* q);
#endif
