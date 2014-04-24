#ifndef RVM_H
#define RVM_H

#include "steque.h"
#include "seqsrchst.h"

/*For undo and redo logs*/
typedef struct mod_t{
  int offset;
  int size;
  void *undo;
} mod_t;

typedef struct _segment_t* segment_t;
typedef struct _redo_t* redo_t;

typedef struct _trans_t* trans_t;
typedef struct _rvm_t* rvm_t;
typedef struct segentry_t segentry_t;

struct _segment_t{
  char segname[128];
  void *segbase;
  int size;
  trans_t cur_trans;
  steque_t mods;
};

struct _trans_t{
  rvm_t rvm;          /*The rvm to which the transaction belongs*/
  int numsegs;        /*The number of segments involved in the transaction*/
  segment_t* segments;/*The array of segments*/
};

/*For redo*/
struct segentry_t{
  char segname[128];
  int segsize;
  int updatesize;
  int numupdates;
  int* offsets;
  int* sizes;
  void *data;
};

/*The redo log */
struct _redo_t{
  int numentries;
  segentry_t* entries;
};


/* rvm */
struct _rvm_t{
  char prefix[128];   /*The path to the directory holding the segments*/
  int redofd;         /*File descriptor for the redo-log*/
  seqsrchst_t segst;  /*A sequential search dictionary mapping base pointers to segment names*/ 
};


/*
 * Initializes the library with the specified directory as backing store.
 */
rvm_t rvm_init(const char *directory);

/*
 * Maps a segment from disk into memory. If the segment does not
 * already exist, then create it and give it size size_to_create. If
 * the segment exists but is shorter than size_to_create, then extend
 * it until it is long enough. It is an error to try to map the same
 * segment twice.
 *
 * This procedure automatically truncates the log to ensure that the mapped data is current.
*/
void *rvm_map(rvm_t rvm, const char *segname, int size_to_create);

/*
 * Unmaps a segment from memory.
 */
void rvm_unmap(rvm_t rvm, void *segbase);

/*
 *  Destroys a segment completely, erasing its backing store. This
 *  function should not be called on a segment that is currently
 *  mapped.
 */
void rvm_destroy(rvm_t rvm, const char *segname);

/*
 * Begins a transaction that will modify the segments listed in
 * segbases. If any of the specified segments is already being
 * modified by a transaction, then the call should will and return
 * (trans_t) -1. Note that trant_t needs to be able to be typecasted
 * to an integer type.
 */
trans_t rvm_begin_trans(rvm_t rvm, int numsegs, void **segbases);

/*
 * Declares that the library is about to modify a specified range of
 * memory in the specified segment. The * segment must be one of the
 * segments specified in the call to rvm_begin_trans. Your library
 * needs to en* sure that the old memory has been saved, in case an
 * abort is executed. It is legal call rvm_about_to_modify multiple
 * times on the same memory area.
 */
void rvm_about_to_modify(trans_t tid, void *segbase, int offset, int size);

/*
 * Commits all changes that have been made within the specified
 * transaction. When the call returns, then enough information should
 * have been saved to disk so that, even if the program crashes, the
 * changes will be seen by the program when it restarts.
 *
 * You will want to use fcntl or some such method. Consult the man
 * pages.
 */
void rvm_commit_trans(trans_t tid);

/*
 * Undoes all changes that have happened within the specified
 * transaction.
 */
void rvm_abort_trans(trans_t tid);

/*
 *  Plays through any committed or aborted items in the log file(s) and shrink the log file(s) as much as * possible.
 */
void rvm_truncate_log(rvm_t rvm);

#endif
