#include "dining.c"

/* No changes are needed to this file*/

double const thinking_to_eating = 0.02;
double const eating_to_thinking = 0.05;

void eat(int phil_id){
  fprintf(stdout,"Philosopher %d eats\n", phil_id);
  while (rand() / (RAND_MAX + 1.0) >= eating_to_thinking);
}

void think(int phil_id){
  fprintf(stdout,"Philosopher %d thinks\n", phil_id);
  while (rand() / (RAND_MAX + 1.0) >= thinking_to_eating);
}

pthread_mutex_t servings_mutex;
int servings;

void* philosodine(void* arg){
  intptr_t phil_id;

  phil_id = (intptr_t) arg;

  while(1){
    /* Philosopher gets served */
    pthread_mutex_lock(&servings_mutex);
    if(servings <= 0){
      pthread_mutex_unlock(&servings_mutex);     
      break;
    }
    else{
      servings--;
      pthread_mutex_unlock(&servings_mutex);     
    }

    /* Picks up his chopsticks */
    pickup_chopsticks(phil_id);

    /* Eats */
    eat(phil_id);

    /* Puts down his chopsticks */
    putdown_chopsticks(phil_id);

    /* And then thinks. */
    think(phil_id);
  }

  return NULL;
}

int main(){
  long i;
  pthread_t phil_threads[5];

  srand(time(NULL));

  pthread_mutex_init(&servings_mutex, NULL);
  servings = 1000;
  
  for(i = 0; i < 5; i++)
    pthread_mutex_init(&chopstick_mutex[i], NULL); 

  for(i = 0; i < 5; i++)
    pthread_create(&phil_threads[i], NULL, philosodine, (void*) i);

  for(i = 0; i < 5; i++)
    pthread_join(phil_threads[i], NULL);    
  
  for(i = 0; i < 5; i++)
    pthread_mutex_destroy(&chopstick_mutex[i]); 

  return 0;
}
