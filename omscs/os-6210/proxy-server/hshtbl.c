#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "hshtbl.h"

static int hshtbl_hv(hshtbl_t* this, char *key){
  int i, ans;

  ans = 0;
  for(i = 0; key[i] != '\0'; i++)
    ans = (31 * ans + key[i]) % this->M;
  
  return ans;
}

int hshtbl_init(hshtbl_t* this, int M){
  int i;

  this->N = 0;
  this->M = M;
  this->keys = (char**) malloc(sizeof(char*) * M);
  this->items = (hshtbl_item*) malloc(sizeof(void*) * M);
  
  for(i = 0; i < M; i++){
    this->keys[i] = NULL;
    this->items[i] = NULL;
  }
  return 0;
} 

void hshtbl_put(hshtbl_t* this, char *key, hshtbl_item item){
  int j;

  if(item == NULL){
    hshtbl_delete(this, key);
    return;
  }

  if(this->N == this->M){
    fprintf(stderr, "Error: Overflow in hshtbl_put.\n");
    exit(EXIT_FAILURE);
   }
    
  for( j = hshtbl_hv(this, key); this->keys[j] != NULL; j = (j + 1) % this->M){
    if( strcmp(key, this->keys[j]) == 0 ){
      this->items[j] = item;
      return;
    }
  }

  this->keys[j] = key;
  this->items[j] = item;
  this->N++;
}

hshtbl_item hshtbl_get(hshtbl_t* this, char *key){
  int j,k;
  
  for( j = hshtbl_hv(this, key), k = 0; this->keys[j] != NULL && k < this->M; j = (j + 1) % this->M, k++)
    if( strcmp(key, this->keys[j]) == 0)
      return this->items[j];
  return NULL;
}

void hshtbl_delete(hshtbl_t* this, char* key){
  int j;
  char* key_to_rehash;
  void *item_to_rehash;

  if( hshtbl_get(this, key) == NULL) 
    return;

  for( j = hshtbl_hv(this,key); strcmp(key, this->keys[j]) != 0; j = (j + 1) % this->M);
  
  this->keys[j] = NULL;
  this->items[j] = NULL;

  j = (j+1) % this->M;
  while(this->keys[j] != NULL){
    key_to_rehash = this->keys[j];
    item_to_rehash = this->items[j];
    this->keys[j] = NULL;
    this->items[j] = NULL;
    this->N--;
    hshtbl_put(this, key_to_rehash, item_to_rehash);
    j = (j+1) % this->M;
  }

  this->N--;
}

void hshtbl_destroy(hshtbl_t* this){
  free(this->keys);
  free(this->items);
}
