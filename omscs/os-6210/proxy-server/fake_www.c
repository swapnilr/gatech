#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include "fake_www.h"
#include "gtcache.h"

void fake_www_init(fake_www* www, char* filename, int flags){
  FILE *fp;
  int i;

  fp = fopen(filename, "r");

  /*Reading the number of urls as the first line in the file*/
  if( fscanf(fp, "%d\n", &www->nurls) != 1 ){
    fprintf(stderr, "Error in reading %s as a webcheat file\n", filename);
    exit(EXIT_FAILURE);
  }
  
  /*Allocating memory*/
  www->urls = (char**) malloc(www->nurls * sizeof(char*));
  www->lengths = (int*) malloc(www->nurls * sizeof(int));

  for(i = 0; i < www->nurls; i++){
    www->urls[i] = (char*) malloc(FAKE_WWW_MAX_URL_LEN);
    if( fscanf(fp, "%s , %d\n", www->urls[i], &www->lengths[i]) != 2 ){
      fprintf(stderr, "Error in reading %s as a webcheat file\n", filename);
      exit(EXIT_FAILURE);
    }
  }
  fclose(fp);
  
  if( (flags & FAKE_WWW_IGNORE_SIZE) > 0){
    for(i = 0; i < www->nurls; i++)
      www->lengths[i] = FAKE_WWW_MIN_CACHE_LEN-1;
  }

  return;

}

void fake_www_get(fake_www *www, char *url, struct MemoryStruct* chunk){
  int i,j;
  
  for(i = 0; i < www->nurls; i++){
    if( strcmp(url, www->urls[i]) == 0 ){
      chunk->size = www->lengths[i];
      
      chunk->memory = (char*) malloc(chunk->size + 1);
      for(j = 0; j < chunk->size; j++)
	chunk->memory[j] = (char) (rand() % 10 + 30);

      /*null-terminating so that it can be interpretted as a string*/
      chunk->memory[chunk->size] = '\0';
      return;
    }
  }

  fprintf(stderr, "url %s not found in fake_www_get\n", url);
  exit(EXIT_FAILURE);
}
