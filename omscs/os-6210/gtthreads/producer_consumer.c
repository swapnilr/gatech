#include <pthread.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>
#include "steque.h"

/* Thread Function Prototypes */
void *producer_routine(void *arg);
void *consumer_routine(void *arg);


/* Global Data */
long g_num_prod = 0; /* number of producer threads */
pthread_mutex_t g_num_prod_lock = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t g_queue_lock = PTHREAD_MUTEX_INITIALIZER;

/* Main - entry point */
int main(int argc, char **argv) {
  steque_t queue;
  pthread_t producer_thread, consumer_thread;
  void *thread_return = NULL;
  int result = 0;

  /* Initialization */

  printf("Main thread started with thread id %"PRIdPTR"\n", (intptr_t) pthread_self());

  steque_init(&queue);

  g_num_prod = 1; /* there will be 1 producer thread */

  /* Create producer and consumer threads */

  result = pthread_create(&producer_thread, NULL, producer_routine, &queue);
  if (0 != result) {
    fprintf(stderr, "Failed to create producer thread: %s\n", strerror(result));
    exit(1);
  }

  printf("Producer thread started with thread id %" PRIdPTR "\n", (intptr_t) producer_thread);

  result = pthread_detach(producer_thread);
  if (0 != result)
    fprintf(stderr, "Failed to detach producer thread: %s\n", strerror(result));

  result = pthread_create(&consumer_thread, NULL, consumer_routine, &queue);
  if (0 != result) {
    fprintf(stderr, "Failed to create consumer thread: %s\n", strerror(result));
    exit(1);
  }

  /* Join threads, handle return values where appropriate */

  result = pthread_join(consumer_thread, &thread_return);
  if (0 != result) {
    fprintf(stderr, "Failed to join consumer thread: %s\n", strerror(result));
    pthread_exit(NULL);
  }

  result = pthread_join(producer_thread, NULL);
  if (0 != result) {
    fprintf(stderr, "Failed to join producer thread: %s\n", strerror(result));
    pthread_exit(NULL);
  }
  
  printf("\nPrinted %"PRIdPTR" characters.\n", (intptr_t) thread_return);
  free(thread_return);

  pthread_mutex_destroy(&g_queue_lock);
  pthread_mutex_destroy(&g_num_prod_lock);
  return 0;
}


/* Function Definitions */

/* producer_routine - thread that adds the letters 'a'-'z' to the queue */
void *producer_routine(void *arg) {
  steque_t *queue_p = arg;
  pthread_t consumer_thread;
  int i, result = 0;
  intptr_t c;

  result = pthread_create(&consumer_thread, NULL, consumer_routine, queue_p);
  if (0 != result) {
    fprintf(stderr, "Failed to create consumer thread: %s\n", strerror(result));
    exit(1);
  }

  result = pthread_detach(consumer_thread);
  if (0 != result)
    fprintf(stderr, "Failed to detach consumer thread: %s\n", strerror(result));

  for (i = 0; i < 100; i++){
    for (c = 'a'; c <= 'z'; ++c) {
      /* Add the node to the queue */
      pthread_mutex_lock(&g_queue_lock);

      steque_enqueue(queue_p, (void*) c);

      pthread_mutex_unlock(&g_queue_lock);

      sched_yield();
    }
  }

  pthread_mutex_lock(&g_num_prod_lock);
  --g_num_prod;
  pthread_mutex_unlock(&g_num_prod_lock);
  return (void*) 0;
}


/* consumer_routine - thread that prints characters off the queue */
void *consumer_routine(void *arg) {
  steque_t *queue_p = arg;
  intptr_t c;
  long count = 0; /* number of nodes this thread printed */

  printf("Consumer thread started with thread id %"PRIdPTR"\n", (intptr_t) pthread_self());

  /* terminate the loop only when there are no more items in the queue
   * AND the producer threads are all done */

  pthread_mutex_lock(&g_queue_lock);
  pthread_mutex_lock(&g_num_prod_lock);

  while(!steque_isempty(queue_p) || g_num_prod > 0) {
    pthread_mutex_unlock(&g_num_prod_lock);

    if (!steque_isempty(queue_p)) {
      c = (intptr_t) steque_pop(queue_p);
      printf("%c", (char) c);
      ++count;
      pthread_mutex_unlock(&g_queue_lock);
    }
    else { /* Queue is empty, so let some other thread run */
      pthread_mutex_unlock(&g_queue_lock);
      sched_yield();
    }
  }
  pthread_mutex_unlock(&g_num_prod_lock);
  pthread_mutex_unlock(&g_queue_lock);

  return (void*) count;
}
