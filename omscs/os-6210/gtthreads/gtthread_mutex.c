/**********************************************************************
gtthread_mutex.c.  

This file contains the implementation of the mutex subset of the
gtthreads library.  The locks can be implemented with a simple queue.
 **********************************************************************/

/*
  Include as needed
*/


#include "gtthread.h"
#include <stdlib.h>
#include <signal.h>
#include <sys/time.h>

static sigset_t vtalrm;

// Block Signals also
int test_and_set(gtthread_mutex_t* mutex, gtthread_t owner) {
  //Block
  sigprocmask(SIG_BLOCK, &vtalrm, NULL);
  if((*mutex) == UNLOCKED) {
    (*mutex) = LOCKED;
    steque_enqueue(&(owner->locks), (steque_item) mutex);
    //Unblock
    sigprocmask(SIG_UNBLOCK, &vtalrm, NULL);
    return 1;
  }
  //Unblock
  sigprocmask(SIG_UNBLOCK, &vtalrm, NULL);
  return 0;
}

void free_mutex(gtthread_mutex_t* mutex, gtthread_t owner) {
  //BLOCK
  sigprocmask(SIG_BLOCK, &vtalrm, NULL);
  *mutex = UNLOCKED;
  while( ( (gtthread_mutex_t*) steque_front(&(owner->locks)) ) != mutex) {
    steque_cycle(&(owner->locks));
  }
  steque_pop(&(owner->locks));
  //UNBLOCK
  sigprocmask(SIG_UNBLOCK, &vtalrm, NULL);
}

/*
  The gtthread_mutex_init() function is analogous to
  pthread_mutex_init with the default parameters enforced.
  There is no need to create a static initializer analogous to
  PTHREAD_MUTEX_INITIALIZER.
 */
int gtthread_mutex_init(gtthread_mutex_t* mutex){
  sigemptyset(&vtalrm);
  sigaddset(&vtalrm, SIGVTALRM);
  sigprocmask(SIG_UNBLOCK, &vtalrm, NULL);
  mutex = (gtthread_mutex_t*) malloc(sizeof(gtthread_mutex_t));
  return 0;
}

/*
  The gtthread_mutex_lock() is analogous to pthread_mutex_lock.
  Returns zero on success.
 */
int gtthread_mutex_lock(gtthread_mutex_t* mutex){
  gtthread_t current = gtthread_self();
  while(!test_and_set(mutex, current)) {
    current->state = WAITING;
    current->waiting_on = mutex;
  }
  //TODO: Add mutex owned to locks
  return 0;
}

/*
  The gtthread_mutex_unlock() is analogous to pthread_mutex_unlock.
  Returns zero on success.
 */
int gtthread_mutex_unlock(gtthread_mutex_t *mutex){
  free_mutex(mutex, gtthread_self());
  return 0;
}

/*
  The gtthread_mutex_destroy() function is analogous to
  pthread_mutex_destroy and frees any resourcs associated with the mutex.
*/
int gtthread_mutex_destroy(gtthread_mutex_t *mutex){
  free(mutex);
  return 0;
}
