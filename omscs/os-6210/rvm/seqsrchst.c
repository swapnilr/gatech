#include<stdlib.h>
#include"seqsrchst.h"

void seqsrchst_init(seqsrchst_t* st, 
		    int (*keyeq)(seqsrchst_key a, seqsrchst_key b)){
  st->first = NULL;
  st->N = 0;
  st->keyeq = keyeq;
}

int seqsrchst_size(seqsrchst_t* st){
  return st->N;
}

int seqsrchst_isempty(seqsrchst_t* st){
  return st->N == 0;
}

int seqsrchst_contains(seqsrchst_t* st, seqsrchst_key key){
  return seqsrchst_get(st, key) == NULL;
}

seqsrchst_value seqsrchst_get(seqsrchst_t* st, seqsrchst_key key){
  seqsrchst_node* node;

  for( node = st->first; node != NULL; node = node->next)
    if(st->keyeq(node->key, key))
      return node->value;
  
  return NULL;
}

seqsrchst_value seqsrchst_delete(seqsrchst_t* st, seqsrchst_key key){
  seqsrchst_value ans;
  seqsrchst_node* node;
  seqsrchst_node* prev;
  
  node = st->first;
  while(node != NULL && !st->keyeq(key, node->key) ){
    prev = node;
    node = node->next;
  }
  
  if (node == NULL)
    return NULL;

  ans = node->value;
  
  if( node == st->first) st->first = node->next;
  else prev->next = node->next;
  st->N--;
  free(node);

  return ans;    
}

void seqsrchst_put(seqsrchst_t* st, seqsrchst_key key, seqsrchst_value value){
  seqsrchst_node* node;

  node = (seqsrchst_node*) malloc(sizeof(seqsrchst_node));
  node->key = key;
  node->value = value;
  node->next = st->first;
  st->first = node;
  st->N++;
}

void seqsrchst_destroy(seqsrchst_t *st){
  seqsrchst_node* node;
  seqsrchst_node* prev;
  
  node = st->first;
  while(node != NULL){
    prev = node;
    node = node->next;
    free(prev);
  }  
}
