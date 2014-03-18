/*
 * Implement an LRU replacement cache policy
 *
 * See the comments in gtcache.h for API documentation.
 *
 * The least recently used element from the cache should be evicted.
 *
 */

#include <stdlib.h>
#include "gtcache.h"
/*
 * Include headers for data structures as you see fit
 */



int gtcache_init(size_t capacity, size_t min_entry_size, int num_levels){


}

void* gtcache_get(char *key, size_t *val_size){

}

int gtcache_set(char *key, void *value, size_t val_size){
 
}

int gtcache_memused(){

}

void gtcache_destroy(){
 
}
