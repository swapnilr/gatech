/*
 * Implement an LFU replacement cache policy
 *
 * See the comments in gtcache.h for API documentation.
 *
 * The entry in the cache with the fewest hits since it entered the
 * cache (the most recent time) is evicted.
 *
 */

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "gtcache.h"
/*
 * Include headers for data structures as you see fit
 */
#include "steque.h"
#include "hshtbl.h"
#include "indexminpq.h"

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
static indexminpq_t* priorityqueue;

int keycmp(indexminpq_key a, indexminpq_key b) {
  int val_a = *((int *) a);
  int val_b = *((int *) b);
  return (val_a < val_b) ? -1 : (val_a > val_b);
}

int gtcache_init(size_t capacity, size_t min_entry_size, int num_levels){
  ////printf("Init called with %lu %lu\n", (long) capacity, (long) min_entry_size);
  long size = capacity/min_entry_size;
  cache_entries = (cache_entry_t *) malloc(size * sizeof(cache_entry_t));
  ////printf("Address of cache_entries %lu\n", (long) cache_entries);  
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
  
  priorityqueue = (indexminpq_t*) malloc(sizeof(indexminpq_t));
  indexminpq_init(priorityqueue, (int) size, &keycmp);
  
  return 0;
}

/*
 *  If in hashtable, get index
 *  cache_entries[index].value
 *  Update hit!
 */
void* gtcache_get(char *key, size_t *val_size){
  //printf("Get called %s %d\n", key, hashtable->N);
  cache_entry_t *savedVal = (cache_entry_t *) hshtbl_get(hashtable, key);
  if(savedVal && strcmp(savedVal->key, key) == 0){
    ////printf("Entry key %s at %lu\n", savedVal->key, (long) savedVal);
    ////printf("%d\n",savedVal->id);
    void *retVal = malloc(savedVal->val_size);
    ////printf("Reached here%s %lu\n", savedVal->key, (long) savedVal->val_size);
    memcpy(retVal, savedVal->value, savedVal->val_size);
    ////printf("Reached here\n");
    *val_size = savedVal->val_size;
    savedVal->hits = savedVal->hits + 1;
    ////printf("Increasing hits for %d from %d to %d\n", savedVal->id, *((int *) indexminpq_keyof(priorityqueue, savedVal->id)), savedVal->hits);
    indexminpq_increasekey(priorityqueue, savedVal->id, (indexminpq_key) &(savedVal->hits));
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
  ////printf("Entry key %s at %lu\n", entry->key, (long) entry);
  hshtbl_put(hashtable, key, entry);
  memused = memused + val_size;
  entry->hits = 1;
  indexminpq_insert(priorityqueue, index, (indexminpq_key) &(entry->hits));
  //printf("Add Entry called %s %d\n", key, index);
}

cache_entry_t* pick_evictee() {
  int index = indexminpq_delmin(priorityqueue);
  //printf("EVICTING %d\n", index);
  return &(cache_entries[index]);
}

void evict(size_t val_size) {
  cache_entry_t* evictee = pick_evictee();
  //printf("Evicting %s at index %d with hits %d\n", evictee->key, evictee->id, evictee->hits);
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

/*
 *  If canAdd() [space in cache + cache entry avail]
 *    Add() {
 *      Pick available cache entry
 *      Update cache_entry_t with value + key + size [make copy of key and value]
 *      Put index in hashtable
 *      Put entry in priority queue
 *      Update memused
 *    }
 *  Else
 *    Evict() {
 *      Pick next to evict[in this case, pop from priority queue]
 *      Add index to stack
 *      Remove entry from hashtable
 *      free(key), free(value) from cache_entries
 *      Update memused
 *      if(canAdd()) {
 *        return;
 *      } else {
 *        Evict();
 *      }
 *    Add()
 */
int gtcache_set(char *key, void *value, size_t val_size){
  ////printf("Set called with %s, %lu\n", key, (long) val_size);
  if(val_size <= cache_capacity) {
    if(spaceAvailable(val_size)) {
      addEntry(key, value, val_size);
    } else {
      evict(val_size);
      addEntry(key, value, val_size);
    }
  }
  //savedVal = malloc(val_size);
  //memcpy(savedVal, value, val_size);
  //val = val_size;
  return 0;
}

int gtcache_memused(){

  return (int) memused;
}

void gtcache_destroy(){
  //printf("Destroy called\n");
  //Clean up everything in cache_entries
  int i;
  for(i=0; i<cache_size; i++) {
    if(cache_entries[i].hits != 0) {
      //printf("Hits %d for %s\n", cache_entries[i].hits, cache_entries[i].key);
      free(cache_entries[i].key);
      free(cache_entries[i].value);
      //printf("DONE\n");
    }
  }
  //printf("Done till here\n");
  free(cache_entries);
  steque_destroy(stack);
  hshtbl_destroy(hashtable);
  indexminpq_destroy(priorityqueue);
}
