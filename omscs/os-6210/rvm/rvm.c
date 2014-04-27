#include"rvm.h"

/*
   Helper file access methods, to lock access while accessing files
 */

/*
  Initialize the library with the specified directory as backing store.
*/
rvm_t rvm_init(const char *directory){
  /*
      1. Create file for redo log with current timestamp -> Get fd
      2. rvm_t should contain
          a. Directory name
          b. fd
          c. New seqsrchst (seg base -> segment)
   */


}
/*
  map a segment from disk into memory. If the segment does not already exist, then create it and give it size size_to_create. If the segment exists but is shorter than size_to_create, then extend it until it is long enough. It is an error to try to map the same segment twice.
*/
void *rvm_map(rvm_t rvm, const char *segname, int size_to_create){
  /*
      1. If segment not present
         a. Create segment file <segname>.seg
         b. malloc memory of size size_to_create -> segbase
      2. If segment present
         a. truncate_log()
         b. Read <segname>.seg -> size, segbase
         c. If size_to_create > size -> realloc segbase
      3. Create segment_t
      4. Add segbase -> segment_t to rvm_t.segst
      5. Return segbase
   */
}

/*
  unmap a segment from memory.
*/
void rvm_unmap(rvm_t rvm, void *segbase){
  /*
      1. Get segment_t from rvm_t.srchst[segbase]
      2. Zero out segment_t queue of modifications
   */
}

/*
  destroy a segment completely, erasing its backing store. This function should not be called on a segment that is currently mapped.
 */
void rvm_destroy(rvm_t rvm, const char *segname){
  /*
      1. Delete <segname>.seg
   */
}

/*
  begin a transaction that will modify the segments listed in segbases. If any of the specified segments is already being modified by a transaction, then the call should fail and return (trans_t) -1. Note that trant_t needs to be able to be typecasted to an integer type.
 */
trans_t rvm_begin_trans(rvm_t rvm, int numsegs, void **segbases){
  /*
      1. Create trans_t with [rvm, numsegs, segment_t[numsegs]]
      2. For cur in 1 to numsegs
         a. Get segment_t = rvm_t.srst[segbase]
         b. trans_t.segments[cur] = segment_t
         c. if segment_t->cur_trans != NULL
            i. Free trans_t
            ii. Return (trans_t) -1
         d. segment_t->trans_t = tid
      3. return tid
   */

}

/*
  declare that the library is about to modify a specified range of memory in the specified segment. The segment must be one of the segments specified in the call to rvm_begin_trans. Your library needs to ensure that the old memory has been saved, in case an abort is executed. It is legal call rvm_about_to_modify multiple times on the same memory area.
*/
void rvm_about_to_modify(trans_t tid, void *segbase, int offset, int size){
  /*
      1. segment_t = tid->rvm.srchst[segbase]
      2. undo = segbase[offset:offset+size]
      3. mod = [offset, size, undo]
      4. segment_t->mods.enqueue(mod)
   */

}

/*
commit all changes that have been made within the specified transaction. When the call returns, then enough information should have been saved to disk so that, even if the program crashes, the changes will be seen by the program when it restarts.
*/
void rvm_commit_trans(trans_t tid){
  /*
     1. Create segentry_t out of each tid->segment->mod
     2. Write segentry_t + data to redo file
     3. Free segentries, mods(+ undo segments) + tid [NOT segment_t]
   */
}

/*
  undo all changes that have happened within the specified transaction.
 */
void rvm_abort_trans(trans_t tid){
  /*
     1. For each tid->segment->mod(in reverse order)
     2. Apply undo segment to offset, size of segbase
     3. Free mods, undo segments, tid
   */

}

/*
 play through any committed or aborted items in the log file(s) and shrink the log file(s) as much as possible.
*/
void rvm_truncate_log(rvm_t rvm){
  /*
     1. Read redo log file to create redo log + segentries
     2. Apply segentries to segname.seg files
     3. Truncate redo log file
     4. Free _redo_t + segentries
   */

}

