#ifndef SEQSRCHST_H
#define SEQSRCHST_H

typedef void* seqsrchst_key;
typedef void* seqsrchst_value;

typedef struct _seqsrchst_node{
  seqsrchst_key key;
  seqsrchst_value value;
  struct _seqsrchst_node* next;
} seqsrchst_node;

typedef struct{
  seqsrchst_node* first;
  int N;
  int (*keyeq)(seqsrchst_key a, seqsrchst_key b);
}seqsrchst_t;

void seqsrchst_init(seqsrchst_t* st, int (*keyeq)(seqsrchst_key a, seqsrchst_key b));
int seqsrchst_size(seqsrchst_t* st);
int seqsrchst_isempty(seqsrchst_t* st);
int seqsrchst_contains(seqsrchst_t* st, seqsrchst_key key);
seqsrchst_value seqsrchst_get(seqsrchst_t* st, seqsrchst_key key);
seqsrchst_value seqsrchst_delete(seqsrchst_t* st, seqsrchst_key key);
void seqsrchst_put(seqsrchst_t* st, seqsrchst_key key, seqsrchst_value value);
void seqsrchst_destroy(seqsrchst_t *st);
#endif
