#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <ctype.h>
#include "fake_www.h"
#include "gtcache.h"

int numlevels(fake_www* www){
  int i, v, maxlen;
  
  maxlen = 0;
  for(i = 0; i < www->nurls; i++){
    if(maxlen < www->lengths[i] + 1)
      maxlen = www->lengths[i] + 1;
  }

  for(i = 1, v = FAKE_WWW_MIN_CACHE_LEN; v < maxlen; i++, v*=2);

  return i;
}

void rstrip(char *str){
  char* end;

  end = str + strlen(str)-1;
  while(end >= str && isspace(*end)) end--;

  *(end+1) = '\0';
  
  return;
}

int main(int argc, char* argv[]){
  struct MemoryStruct chunk;
  char url[FAKE_WWW_MAX_URL_LEN];
  char *data, *res;
  int i, hits, misses, Npts, started;
  int min_cache_sz, max_cache_sz, cache_sz;
  int num_requests, nlevels, urlcount;
  
  fake_www www;
  size_t sz;

  if(argc < 3){
    fprintf(stderr,"Usage: cache_test [FAKE_WWW] [NUM_REQUESTS] \n");
    exit(0);
  }

  srand(12314);

  fake_www_init(&www, argv[1], 0);
  num_requests = strtol(argv[2], NULL, 10);
  Npts = 20;

  /*Setting minimum and maximum cache sizes*/
  min_cache_sz = 1 << 20;
  max_cache_sz = 1 << 24;
  nlevels = numlevels(&www);
  
  for(i = 0; i < Npts; i++){
    /*Cache sizes go up on a logarithmic scale*/
    cache_sz = (int) (min_cache_sz * pow( 1.0 * max_cache_sz / min_cache_sz, 1.0 * i / (Npts-1)));

    gtcache_init(cache_sz, FAKE_WWW_MIN_CACHE_LEN, nlevels);

    hits = 0;
    misses = 0;
    started = 0;
    urlcount = 0;
    rewind(stdin);
    while(hits + misses < num_requests){

      res = fgets(url, FAKE_WWW_MAX_URL_LEN, stdin);
      if (res == NULL){
	if(!feof(stdin)){
	  /*We should always be able to read from the file*/
	  fprintf(stderr, "Error parsing the list of requests\n");
	  exit(EXIT_FAILURE);
	}
	else{
	  /*Rewind to the beginning if we've reached the end*/
	  started = 1;
	  rewind(stdin);
	  if( urlcount == 0 ){
	    fprintf(stderr, "No valid requests in the input file.\n");
	    exit(EXIT_FAILURE);
	  }
	      
	  urlcount = 0;
	  continue;
	}
      }

      /*Treat lines starting in # as comments*/
      if (url[0] == '#')
	continue;

      /*Stripping url of any trailing whitespace*/
      rstrip(url);
      if(strlen(url) == 0)
	continue;

      urlcount++;
      data = gtcache_get(url, &sz);
    
      if(data != NULL){
	/*Cache hit!*/
	hits+= started;
	free(data);
      }
      else{
	/*Cache miss!*/
	misses+= started;

	fake_www_get(&www, url, &chunk);
	
	/*Accounting for cold start.  Only once the cache_size is reached do we start counting*/
	if( gtcache_memused() + chunk.size + 1> cache_sz)
	  started = 1;

	gtcache_set(url, chunk.memory, chunk.size + 1);

	free(chunk.memory);
      }
    }

    gtcache_destroy();

    printf("%d\t%f\n", cache_sz, 1.0*hits/(hits + misses));
  }

  return 0;
}
