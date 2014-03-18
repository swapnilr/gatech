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
