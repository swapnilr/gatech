/*
 * Implement an LRUMIN replacement cache policy
 *
 * See the comments in gtcache.h for API documentation.
 *
 * The LRUMIN eviction should be equivalent to the 
 * following psuedocode.
 *
 * while more space needs to be cleared
 *   Let n be the smallest integer such that 2^n >= space needed
 *   If there is an entry of size >= 2^n,
 *      delete the least recently used entry of size >= 2^n
 *   Otherwise, let m be the smallest inetger such that there an entry of size >= 2^m
 *     delete the least recently used item of size >=2^m
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
#include "indexminpq.h"

typedef struct cache_entry_t {
  size_t val_size;
  char *key;
  char *value;
  int id;
  int hits;
  long lastTime;
} cache_entry_t;

typedef struct queue {
  indexminpq_t* priorityqueue;
  size_t lower_bound;
  size_t upper_bound;
} queue;

static cache_entry_t *cache_entries;
static size_t cache_capacity;
static long cache_size;
static size_t memused;
static steque_t* stack;
static hshtbl_t* hashtable;
static queue* queues;
static int levels;

int keycmp(indexminpq_key a, indexminpq_key b) {
  long val_a = *((long *) a);
  long val_b = *((long *) b);
  return (val_a < val_b) ? -1 : (val_a > val_b);
}

int gtcache_init(size_t capacity, size_t min_entry_size, int num_levels){
  long size = capacity/min_entry_size;
  cache_entries = (cache_entry_t *) malloc(size * sizeof(cache_entry_t));
  cache_capacity = capacity;
  cache_size = size;
  memused = 0;
  levels = num_levels;
  
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
  
  queues = (queue *) malloc(num_levels * sizeof(queue));
  size_t lower = 0;
  for(i=0; i<num_levels; i++) {
    queues[i].priorityqueue = (indexminpq_t*) malloc(sizeof(indexminpq_t));
    indexminpq_init(queues[i].priorityqueue, (int) size, &keycmp);
    queues[i].lower_bound = lower;
    size_t upper = 2 * lower;
    if(i == num_levels - 1) {
      upper = capacity;
    } else if(lower == 0) {
      upper = 2 * min_entry_size;
    }
    queues[i].upper_bound = upper;
    lower = upper;
  }
  
  return 0;
}

int get_queue_index(size_t val_size) {
  int i;
  for(i=0; i<levels; i++) {
    if(val_size <= queues[i].upper_bound) {
      return i;
    }
  }
  return -1;
}

void* gtcache_get(char *key, size_t *val_size){
  cache_entry_t *savedVal = (cache_entry_t *) hshtbl_get(hashtable, key);
  if(savedVal && strcmp(savedVal->key, key) == 0){
    void *retVal = malloc(savedVal->val_size);
    memcpy(retVal, savedVal->value, savedVal->val_size);
    *val_size = savedVal->val_size;
    savedVal->hits = savedVal->hits + 1;
    struct timeval start;
    gettimeofday(&start, NULL);
    savedVal->lastTime = (long)(start.tv_sec * 1000000 + start.tv_usec);
    indexminpq_changekey(queues[get_queue_index(savedVal->val_size)].priorityqueue, savedVal->id, (indexminpq_key) &(savedVal->lastTime));
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
  struct timeval start;
  gettimeofday(&start, NULL);
  entry->lastTime = (long)(start.tv_sec * 1000000 + start.tv_usec);
  indexminpq_insert(queues[get_queue_index(entry->val_size)].priorityqueue, index, (indexminpq_key) &(entry->lastTime));
}

cache_entry_t* pick_evictee(size_t val_size) {
  /*
   * Go from Queue to highest queue
   */
  int index = -1;
  int queue_index = get_queue_index(val_size);
  int i;
  for(i=queue_index+1; i<levels; i++) {
    if(!indexminpq_isempty(queues[i].priorityqueue)) {
      index = indexminpq_delmin(queues[i].priorityqueue);
      return &(cache_entries[index]);  
    } 
  }
  
  /* 
   * Otherwise go downwards
   */
  if(index == -1) {
    for(i=queue_index; i>=0; i--) {
      if(!indexminpq_isempty(queues[i].priorityqueue)) {
        index = indexminpq_delmin(queues[i].priorityqueue);
        return &(cache_entries[index]);
      }
    }
  }
   
  return &(cache_entries[index]);
}

void evict(size_t val_size) {
  cache_entry_t* evictee = pick_evictee(val_size);
  steque_enqueue(stack, evictee->id);
  hshtbl_delete(hashtable, evictee->key);
  memused = memused - evictee->val_size;
  evictee->hits=0;
  free(evictee->key);
  free(evictee->value);
  if(!spaceAvailable(val_size)) {
    evict(val_size-(cache_capacity-memused));
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
 
  for(i=0; i<levels; i++) {
    indexminpq_destroy(queues[i].priorityqueue);
  }
  
  free(queues);
}
