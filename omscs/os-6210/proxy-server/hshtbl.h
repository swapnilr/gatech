/*
 * Interface for a string-indexed open-addressing hashtabl.
 */

#ifndef HSHTBL_H
#define HSHTBL_H

typedef void* hshtbl_item;

typedef struct{
  int M;
  int N;
  char** keys;
  hshtbl_item* items;
} hshtbl_t;

/*
 * Iinitializes the (already allocated) hshtable data structure,
 * giving it capacity M.  Typically, M should be at least twice the
 * number of elements that are expected to be stored in the cache.
 */
int hshtbl_init(hshtbl_t* this, int M);


/*
 * Returns the element associated with key
 */
hshtbl_item hshtbl_get(hshtbl_t* this, char *key);

/*
 * Associates item with the string key.
 */
void hshtbl_put(hshtbl_t* this, char *key, hshtbl_item item);


/*
 * Deletes the item associated with key from the hashtable
 */
void hshtbl_delete(hshtbl_t* this, char* key);

/*
 * Frees memory associated with this.
 */
void hshtbl_destroy(hshtbl_t* this);

#endif
