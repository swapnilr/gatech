#ifndef GTTHREAD_H
#define GTTHREAD_H

#include "steque.h"
#include <ucontext.h>

/* Define gtthread_t and gtthread_mutex_t types here */
typedef enum {WAITING, READY, CANCELED, FINISHED} state_t;
typedef struct __gtthread_t __gtthread_t;
typedef __gtthread_t* gtthread_t;
typedef struct __gtthread_t {
  gtthread_t parent;
  ucontext_t context;
  state_t state;
  gtthread_t joiner;
  gtthread_t joining_on;
  void *retval;
  int children;  
} __gtthread_t;

typedef int gtthread_mutex_t;

void gtthread_init(long period);
int  gtthread_create(gtthread_t *thread,
                     void *(*start_routine)(void *),
                     void *arg);
int  gtthread_join(gtthread_t thread, void **status);
void gtthread_exit(void *retval);
void gtthread_yield(void);
int  gtthread_equal(gtthread_t t1, gtthread_t t2);
int  gtthread_cancel(gtthread_t thread);
gtthread_t gtthread_self(void);


int  gtthread_mutex_init(gtthread_mutex_t *mutex);
int  gtthread_mutex_lock(gtthread_mutex_t *mutex);
int  gtthread_mutex_unlock(gtthread_mutex_t *mutex);
int  gtthread_mutex_destroy(gtthread_mutex_t *mutex);
#endif
