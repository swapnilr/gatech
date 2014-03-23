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
  ////////printf("Init called with %lu %lu\n", (long) capacity, (long) min_entry_size);
  //fprintf(stderr, "==================================================================================\n");
  long size = capacity/min_entry_size;
  cache_entries = (cache_entry_t *) malloc(size * sizeof(cache_entry_t));
  ////////printf("Address of cache_entries %lu\n", (long) cache_entries);  
  cache_capacity = capacity;
  //fprintf(stderr, "Cache capacity set to %lu\n", cache_capacity);
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
  
  //fprintf(stderr, "There are %d levels\n", levels);
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
    //fprintf(stderr, "Level %d from %lu to %lu\n", i+1, lower, upper);
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

/*
 *  If in hashtable, get index
 *  cache_entries[index].value
 *  Update hit!
 */
void* gtcache_get(char *key, size_t *val_size){
  //fprintf(stderr, "Get called %s %d\n", key, hashtable->N);
  cache_entry_t *savedVal = (cache_entry_t *) hshtbl_get(hashtable, key);
  if(savedVal && strcmp(savedVal->key, key) == 0){
    ////fprintf(stderr, "Entry key %s at %lu\n", savedVal->key, (long) savedVal);
    ////fprintf(stderr, "%d\n",savedVal->id);
    void *retVal = malloc(savedVal->val_size);
    ////fprintf(stderr, "Reached here %s %lu\n", savedVal->key, (long) savedVal->val_size);
    memcpy(retVal, savedVal->value, savedVal->val_size);
    //printf("Reached here\n");
    *val_size = savedVal->val_size;
    savedVal->hits = savedVal->hits + 1;
    struct timeval start;
    gettimeofday(&start, NULL);
    savedVal->lastTime = (long)(start.tv_sec * 1000000 + start.tv_usec);
    //printf("Increasing key for %d from %d to %d\n", savedVal->id, *((int *) indexminpq_keyof(priorityqueue, savedVal->id)), (int) start.tv_sec);
    //printf("Increasing key for %d from %lu to %lu\n", savedVal->id, *((long *) indexminpq_keyof(priorityqueue, savedVal->id)), savedVal->lastTime);
    //printf("Checking in queue %d for %s(index %d) with val %lu\n", get_queue_index(savedVal->val_size) ,savedVal->key, savedVal->id, (long) savedVal->val_size);
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
  ////////printf("Entry key %s at %lu\n", entry->key, (long) entry);
  hshtbl_put(hashtable, key, entry);
  memused = memused + val_size;
  entry->hits = 1;
  struct timeval start;
  gettimeofday(&start, NULL);
  entry->lastTime = (long)(start.tv_sec * 1000000 + start.tv_usec);
  ////printf("Setting key for %d to %lu\n", entry->id, entry->lastTime);
  indexminpq_insert(queues[get_queue_index(entry->val_size)].priorityqueue, index, (indexminpq_key) &(entry->lastTime));
  //printf("Add Entry called %s %d\n", key, index);
}

/*
 * Needs to pick the evictee and handle everything related to the queue(s)
 */
cache_entry_t* pick_evictee(size_t val_size) {
  /*
   * Go from Queue to highest queue
   */
  int index = -1;
  int queue_index = get_queue_index(val_size);
  //fprintf(stderr, "Got queue index %d in levels %d\n", queue_index, levels);
  int i;
  for(i=queue_index+1; i<levels; i++) {
    if(!indexminpq_isempty(queues[i].priorityqueue)) {
      index = indexminpq_delmin(queues[i].priorityqueue);
      //fprintf(stderr, "AHHHHH FIRST Just deleted %d from %d\n", index, i);
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
        //fprintf(stderr, "AHHHHH SECOND Just deleted %d from %d\n", index, i);
        return &(cache_entries[index]);
      }
    }
  }
   
  ////fprintf(stderr, "!!!!!!!!!EVICTING %d from queue %d\n", index, i);
  return &(cache_entries[index]);
}

void evict(size_t val_size) {
  //fprintf(stderr, "Looking for %lu space with %lu used of %lu\n", (long) val_size, (long) memused, (long) cache_capacity);
  cache_entry_t* evictee = pick_evictee(val_size);
  //fprintf(stderr, "-------------Evicting %s at index %d with size %lu\n", evictee->key, evictee->id, (long) evictee->val_size);
  //fprintf(stderr, "%d items left now!\n", hashtable->N);
  steque_enqueue(stack, evictee->id);
  hshtbl_delete(hashtable, evictee->key);
  memused = memused - evictee->val_size;
  evictee->hits=0;
  free(evictee->key);
  free(evictee->value);
  //fprintf(stderr, "Space is now %lu\n", (long) memused);
  if(!spaceAvailable(val_size)) {
    //fprintf(stderr, "NEED MORE SPACE\n");
    evict(val_size-(cache_capacity-memused));
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
  //fprintf(stderr, "Set called with %s, %lu\n", key, (long) val_size);
  if(val_size <= cache_capacity) {
    if(spaceAvailable(val_size)) {
      addEntry(key, value, val_size);
    } else {
      //fprintf(stderr, "Looks like cache at capacity %lu and memused %ld is full\n", (long) cache_capacity, (long) memused);
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
  //////printf("Destroy called\n");
  //Clean up everything in cache_entries
  int i;
  for(i=0; i<cache_size; i++) {
    if(cache_entries[i].hits != 0) {
      //////printf("Hits %d for %s\n", cache_entries[i].hits, cache_entries[i].key);
      free(cache_entries[i].key);
      free(cache_entries[i].value);
      //////printf("DONE\n");
    }
  }
  //////printf("Done till here\n");
  free(cache_entries);
  steque_destroy(stack);
  hshtbl_destroy(hashtable);
 
  for(i=0; i<levels; i++) {
    indexminpq_destroy(queues[i].priorityqueue);
  }
  
  free(queues);
}
