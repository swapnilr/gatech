/*
 * Implement a random replacement cache policy
 *
 * See the comments in gtcache.h for API documentation.
 *
 * An entry from the cache is chosen uniformly at random to be evicted.
 */ 

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/time.h>
#include "gtcache.h"
/*
 * Include headers for data structures as you see fit
 */
#include "steque.h"
#include "hshtbl.h"
#include "indexrndq.h"

typedef struct cache_entry_t {
  size_t val_size;
  char *key;
  char *value;
  int id;
  int hits;
} cache_entry_t;

static cache_entry_t *cache_entries;
static size_t cache_capacity;
static long cache_size;
static size_t memused;
static steque_t* stack;
static hshtbl_t* hashtable;
static indexrndq_t* queue;


int gtcache_init(size_t capacity, size_t min_entry_size, int num_levels){
  long size = capacity/min_entry_size;
  cache_entries = (cache_entry_t *) malloc(size * sizeof(cache_entry_t));
  cache_capacity = capacity;
  cache_size = size;
  memused = 0;
  
  // Initialize data structures
  stack = (steque_t *) malloc(sizeof(steque_t));
  steque_init(stack);
  int i;
  for(i=0; i<size; i++) {
    steque_push(stack, (steque_item) i);
    cache_entries[i].hits=0;
  }
  
  hashtable = (hshtbl_t *) malloc(sizeof(hshtbl_t));
  hshtbl_init(hashtable, 2 * (int) size);
  
  queue = (indexrndq_t*) malloc(sizeof(indexrndq_t));
  indexrndq_init(queue, (int) size);
  
  return 0;
}

void* gtcache_get(char *key, size_t *val_size){
  cache_entry_t *savedVal = (cache_entry_t *) hshtbl_get(hashtable, key);
  if(savedVal && strcmp(savedVal->key, key) == 0){
    void *retVal = malloc(savedVal->val_size);
    memcpy(retVal, savedVal->value, savedVal->val_size);
    *val_size = savedVal->val_size;
    return retVal;
  }
  return (void *) NULL;
}

int spaceAvailable(size_t val_size) {
  return (val_size + gtcache_memused() <= cache_capacity) && !steque_isempty(stack);
}

void addEntry(char *key, char *value, size_t val_size) {
  int index = (int) steque_pop(stack);
  cache_entry_t* entry = &(cache_entries[index]);
  entry->id = index;
  entry->key = strdup(key);
  entry->value = (char *) malloc(val_size);
  entry->val_size = val_size;
  memcpy(entry->value, value, val_size);
  hshtbl_put(hashtable, key, entry);
  memused = memused + val_size;
  entry->hits = 1;
  indexrndq_enqueue(queue, index);
}

cache_entry_t* pick_evictee() {
  int index = indexrndq_dequeue(queue);
  return &(cache_entries[index]);
}

void evict(size_t val_size) {
  cache_entry_t* evictee = pick_evictee();
  steque_enqueue(stack, evictee->id);
  hshtbl_delete(hashtable, evictee->key);
  memused = memused - evictee->val_size;
  evictee->hits=0;
  free(evictee->key);
  free(evictee->value);
  if(!spaceAvailable(val_size)) {
    evict(val_size);
  }

}

int gtcache_set(char *key, void *value, size_t val_size){
  if(val_size <= cache_capacity) {
    if(spaceAvailable(val_size)) {
      addEntry(key, value, val_size);
    } else {
      evict(val_size);
      addEntry(key, value, val_size);
    }
  }
  return 0;
}

int gtcache_memused(){

  return (int) memused;
}

void gtcache_destroy(){
  //Clean up everything in cache_entries
  int i;
  for(i=0; i<cache_size; i++) {
    if(cache_entries[i].hits != 0) {
      free(cache_entries[i].key);
      free(cache_entries[i].value);
    }
  }
  free(cache_entries);
  steque_destroy(stack);
  hshtbl_destroy(hashtable);
  indexrndq_destroy(queue);
}
