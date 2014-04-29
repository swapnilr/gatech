/***
 *** Recoverable Virtual Memory
 *** This file represents the implementation of a recoverable virtual memory, as explained in the LRVM paper.
 *** Each segment is backed in the directory be a <segment_name>.seg file.
 *** Segment File Format: size[int]#data[binary data]
 *** Redo File Format: 
 *** entries[int]#segentry[segname[char[128]]#segsize[int]#updatesize[int]#numupdates[int]#offsets[int#int..]#sizes[int#int..]#data[binarydata]]
 *** # for clarity only, not in actual file
 *** The rvm is backed by a rvm.redo file in the same directory.
 ***/

#include "rvm.h"
#include <fcntl.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>
#include <stdio.h> // for printf
#include <stdint.h>

//TODO: Full malloc + free, cleaning up metadata stuff, like segment_t, close fd, thread protecting file access, move file access methods up here
/*
   Helper file access methods, to lock access while accessing files
 */


/*
 * Helper method to concat 2 strings(for creating full filename)
 */
char *concat(const char* str1, const char* str2) {
   size_t lenDir = strlen(str1);
   size_t lenFile = strlen(str2);
   char *fullFN = malloc(lenDir + lenFile + 1);
   strcpy(fullFN, str1);
   strcat(fullFN, str2);
   return fullFN;
}

/*
 * Helper method to create Segment File Name
 */
char *segFileName(rvm_t rvm, const char* segname) {
  char *segFN = concat(segname, ".seg");
  char *suffix = concat("/", segFN);
  char *fileName = concat(rvm->prefix, suffix);
  free(segFN);
  free(suffix);
  return fileName;
}

/*
 * Equals method for the sequential search dictionary
 */
int equals(seqsrchst_key a, seqsrchst_key b) {
  return a==b;
}


/*
  Initialize the library with the specified directory as backing store.
*/
rvm_t rvm_init(const char *directory){
   // Create redo file
   char *fullFN = concat(directory, "/rvm.redo");
   int fd = open(fullFN, O_RDWR | O_CREAT, S_IRWXU | S_IRGRP | S_IROTH);
   free(fullFN);
   off_t o = lseek(fd, 0, SEEK_END);
   
   // Initialize file with 0 size. 
   // Nothing in redo file right now
   if(o == 0) {
     int size = 0;
     write(fd, &size, sizeof(int));
   }
   
   // Create rvm_t representing the rvm
   rvm_t rvm = (rvm_t) malloc(sizeof(struct _rvm_t));
   strcpy(rvm->prefix, directory);
   rvm->redofd = fd;
   rvm->segst = *((seqsrchst_t *) malloc(sizeof(seqsrchst_t)));
   seqsrchst_init(&(rvm->segst), &equals);

   return rvm;
}
/*
  map a segment from disk into memory. If the segment does not already exist, then create it and give it size size_to_create. If the segment exists but is shorter than size_to_create, then extend it until it is long enough. It is an error to try to map the same segment twice.
*/
void *rvm_map(rvm_t rvm, const char *segname, int size_to_create){
  // Lazy strategy, truncate log on map
  rvm_truncate_log(rvm);

  void *segbase;

  // Check if file is present for the segment
  char *segFN = segFileName(rvm, segname);
  struct stat st;
  int result = stat(segFN, &st);
  if(result == 0) {
    // File is present
    // Open file and read in size
    int fd = open(segFN, O_RDWR | O_CREAT, S_IRWXU | S_IRGRP | S_IROTH);
    void *sizeBuffer = malloc(sizeof(int));
    int retVal = read(fd, sizeBuffer, sizeof(int));
    if(retVal == -1) {
      fprintf(stderr, "ERROR while trying to read size from segment file");
      exit(1);
    }
    int size = (int) *((int *) sizeBuffer);
    
    // Read size amount of bytes into the in memory buffer
    segbase = malloc(size);
    retVal = read(fd, segbase, size);
    if (retVal == -1) {
      fprintf(stderr, "ERROR while trying to read segment file");
      exit(1);
    }
    
    // If bigger buffer is asked for, resize
    if(size_to_create > size) {
       realloc(segbase, size_to_create);
    } else {
      // If segment is actually bigger than asked for, segment metadata(segment_t) should be accurate
      size_to_create = size;
    }
  } else {
    // File is not Present
    // Create file and write 0 buffer into it
    int fd = open(segFN, O_RDWR | O_CREAT, S_IRWXU | S_IRGRP | S_IROTH);
    void* sizeBuffer;
    int size = 0;
    sizeBuffer = (void *) (&size);
    write(fd, sizeBuffer, sizeof(int));
    segbase = malloc(size_to_create);
  }

  // Create segment_t
  segment_t segment = (segment_t) malloc(sizeof(struct _segment_t));
  strcpy(segment->segname, segname);
  segment->segbase = segbase;
  segment->size = size_to_create;
  segment->cur_trans = NULL;
  steque_t* mods = (steque_t *) malloc(sizeof(steque_t));
  steque_init(mods);
  segment->mods = *mods;
  
  // Add segbase -> segment_t to rvm_t.segst
  seqsrchst_put(&(rvm->segst), segbase, segment);

  return segbase;
}

/*
  unmap a segment from memory.
*/
void rvm_unmap(rvm_t rvm, void *segbase){
  // Get segment_t for the given segbase
  segment_t segment = seqsrchst_get(&(rvm->segst), segbase);
  
  // Undo all modifications
  // We need to apply the modifications in reverse order. This is important in case there are 2 overlapping segment modifications, for example:
  // Mod 1: "hello, world" -> "hello, earth". Undo log is "hello, world"
  // Mod 2: "hello, earth" -> "hello, venus". Undo log is "hello, earth"
  // If we apply the first undo log, it becomes "hello, world", then we apply the second undo log, it becomes "hello, earth". WRONG!
  // Since steque only provides the pop method for access(no dequeue), we cycle by pop-ing from the mods queue and *push*ing on a temp queue
  steque_t* mods = &(segment->mods);
  steque_t* temp = (steque_t*) malloc(sizeof(steque_t));
  steque_init(temp);
  // Reverse order of mods
  while(!(steque_isempty(mods))) {
    steque_push(temp, steque_pop(mods));
  }
  // temp now has mods in reverse order, can just apply the undo segments now
  while(!(steque_isempty(temp))) {
    mod_t* mod = steque_pop(temp);
    memcpy((segbase + mod->offset), mod->undo, mod->size);
    free(mod->undo);
    free(mod);
  }
}

/*
  destroy a segment completely, erasing its backing store. This function should not be called on a segment that is currently mapped.
 */
void rvm_destroy(rvm_t rvm, const char *segname){
  // Delete <segname>.seg
  char* segFN = segFileName(rvm, segname);
  remove(segFN);
  free(segFN);
}

/*
  begin a transaction that will modify the segments listed in segbases. If any of the specified segments is already being modified by a transaction, then the call should fail and return (trans_t) -1. Note that trant_t needs to be able to be typecasted to an integer type.
 */
trans_t rvm_begin_trans(rvm_t rvm, int numsegs, void **segbases){
   // Create trans_t
   trans_t trans = (trans_t) malloc(sizeof(struct _trans_t));
   trans->rvm = rvm;
   trans->numsegs = numsegs;
   trans->segments = (segment_t*) malloc(numsegs * sizeof(segment_t));
   int cur;

   // For each segbase, get the segment_t and put in the segment_t array for the transaction
   for(cur=0; cur<numsegs; cur++) {
     void* segbase = segbases[cur];
     segment_t current_segment = seqsrchst_get(&(rvm->segst), segbase);
     if(current_segment->cur_trans != NULL) {
       // ERROR. Need to rollback and update the segment_t's to indicate they are in no active transaction
       for(cur=cur-1; cur>=0; cur--) {
         segbase = segbases[cur];
         current_segment = seqsrchst_get(&(rvm->segst), segbase);
         current_segment->cur_trans = NULL;
       }
       free(trans->segments);
       free(trans);
       return (trans_t) -1;
     } else {
       current_segment->cur_trans = trans;
       trans->segments[cur]=current_segment;
     }
   }
   return trans;
}

/*
  declare that the library is about to modify a specified range of memory in the specified segment. The segment must be one of the segments specified in the call to rvm_begin_trans. Your library needs to ensure that the old memory has been saved, in case an abort is executed. It is legal call rvm_about_to_modify multiple times on the same memory area.
*/
void rvm_about_to_modify(trans_t tid, void *segbase, int offset, int size){
  // Create the undo log
  segment_t segment = seqsrchst_get(&(tid->rvm->segst), segbase);
  void* undo = malloc(size);
  memcpy(undo, (segbase + offset), size);
  mod_t* mod = (mod_t *) malloc(sizeof(mod_t));
  mod->offset = offset;
  mod->size = size;
  mod->undo = undo;
  // Add mod with undo log to queue of mods
  steque_enqueue(&(segment->mods), (steque_item) mod);
}

/*
commit all changes that have been made within the specified transaction. When the call returns, then enough information should have been saved to disk so that, even if the program crashes, the changes will be seen by the program when it restarts.
*/
void rvm_commit_trans(trans_t tid){
  int segmentId;
  int fd = tid->rvm->redofd;

  // Get number of entries that are in the file. We read this number so we can update it, and that can be used in truncate_log
  lseek(fd, 0, SEEK_SET);
  void* sizeBuffer;
  sizeBuffer = malloc(sizeof(int));
  read(fd, sizeBuffer, sizeof(int));
  int entries = *((int*) sizeBuffer);
  
  // Write segentries in the end
  lseek(fd, 0, SEEK_END);
  for(segmentId=0; segmentId < tid->numsegs; segmentId++) {
    segment_t segment = tid->segments[segmentId];

    // Create segentry from segment
    segentry_t* segentry = (segentry_t*) malloc(sizeof(segentry_t));
    strcpy(segentry->segname, segment->segname);
    segentry->segsize = segment->size;
    int size = steque_size(&(segment->mods));
    segentry->numupdates = size;
    segentry->offsets = (int*) malloc(size * sizeof(int));
    segentry->sizes = (int*) malloc(size * sizeof(int));
    segentry->updatesize = 0;
    segentry->data = NULL;

    // Collate mods together in data
    int update = 0;
    while(!(steque_isempty(&(segment->mods)))) {
      mod_t* mod = steque_pop(&(segment->mods));
      int currentsize = segentry->updatesize;
      segentry->updatesize = segentry->updatesize + mod->size;
      segentry->data = realloc(segentry->data, segentry->updatesize);
      segentry->offsets[update] = mod->offset;
      segentry->sizes[update] = mod->size;
      memcpy((segentry->data + currentsize), 
             (segment->segbase + mod->offset), mod->size);
      free(mod->undo);
      free(mod);
      update++;
    }

    // Write segentry to file
    write(fd, &(segentry->segname), 128*sizeof(char));
    write(fd, &(segentry->segsize), sizeof(int));
    write(fd, &(segentry->updatesize), sizeof(int));
    write(fd, &(segentry->numupdates), sizeof(int));
    write(fd, segentry->offsets, segentry->numupdates * sizeof(int));
    write(fd, segentry->sizes, segentry->numupdates * sizeof(int));
    write(fd, segentry->data, segentry->updatesize);
    segment->cur_trans=NULL;
    entries++;
  }
  // Update number of entries
  lseek(fd, 0, SEEK_SET);
  write(fd, &entries, sizeof(int));
  free(tid);
}

/*
  undo all changes that have happened within the specified transaction.
 */
void rvm_abort_trans(trans_t tid){
  // Unmmap all segments in transaction(automatically applies undo logs)
  int segmentId;
  for(segmentId=0; segmentId < tid->numsegs; segmentId++){
    segment_t segment = tid->segments[segmentId];
    rvm_unmap(tid->rvm, segment->segbase);
    segment->cur_trans = NULL;
  }
  free(tid);
}

/*
 play through any committed or aborted items in the log file(s) and shrink the log file(s) as much as possible.
*/
void rvm_truncate_log(rvm_t rvm){
  int fd = rvm->redofd;

  // Read how many segentries there are
  lseek(fd, 0, SEEK_SET);
  void* sizeBuffer = malloc(sizeof(int));
  read(fd, sizeBuffer, sizeof(int));
  int size = *((int *) sizeBuffer);
  
  // For each entry, read and construct segentry_t
  int entry;
  for(entry=0; entry<size; entry++) {
    // Primary metadata
    segentry_t* segentry = (segentry_t *) malloc(sizeof(segentry_t));
    read(fd, &(segentry->segname), 128 * sizeof(char));
    read(fd, &(segentry->segsize), sizeof(int));
    read(fd, &(segentry->updatesize), sizeof(int));
    read(fd, &(segentry->numupdates), sizeof(int));
    // Mod offsets, sizes and collected data
    segentry->offsets = (int*) malloc((segentry->numupdates) * sizeof(int));
    segentry->sizes = (int*) malloc(segentry->numupdates * sizeof(int));
    read(fd, segentry->offsets, segentry->numupdates * sizeof(int));
    read(fd, segentry->sizes, segentry->numupdates * sizeof(int));
    segentry->data = malloc(segentry->updatesize);
    read(fd, segentry->data, segentry->updatesize);

    // Open segment file
    char *segFN = segFileName(rvm, segentry->segname);
    int segFD = open(segFN, O_RDWR | O_CREAT, S_IRWXU | S_IRGRP | S_IROTH);
    // Read size first and then read that much into segbase
    void *sizeBuffer = malloc(sizeof(int));
    int retVal = read(segFD, sizeBuffer, sizeof(int));
    if(retVal == -1) {
      fprintf(stderr, "ERROR while trying to read size from segment file");
      exit(1);
    }
    int size = *((int *) sizeBuffer);
    void* segbase = malloc(size);
    retVal = read(segFD, segbase, size);
    if (retVal == -1) {
      fprintf(stderr, "ERROR while trying to read segment file");
      exit(1);
    }

    // TODO: See what happens if updates are at the end? How do they work?

    // Realloc segbase if the updated segment is larger than the segment read from the file
    if(segentry->segsize > size) {
      segbase = realloc(segbase, segentry->segsize);
      size = segentry->segsize;
    }

    // Applying Updates in memory
    int dataOffset = 0;
    int update;
    for(update=0; update<segentry->numupdates; update++) {
      memcpy((segbase + segentry->offsets[update]), 
             (segentry->data + dataOffset), segentry->sizes[update]);
      dataOffset = dataOffset + segentry->sizes[update];
    }

    // Write updates to segment file
    lseek(segFD, 0, SEEK_SET);
    write(segFD, &size, sizeof(int));
    write(segFD, segbase, size);
    free(segentry->offsets);
    free(segentry->sizes);
    free(segentry->data);
    free(segentry);

    close(segFD);
  }
  
  // Now that the updates have been applied, truncate redo log file
  close(fd);
  char *fullFN = concat(rvm->prefix, "/rvm.redo");
  remove(fullFN);
  fd = open(fullFN, O_RDWR | O_CREAT, S_IRWXU | S_IRGRP | S_IROTH);
  rvm->redofd = fd;
  int zsize = 0;
  write(fd, &zsize, sizeof(int));
}

