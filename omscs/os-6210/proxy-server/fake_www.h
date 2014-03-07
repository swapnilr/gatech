#ifndef FAKE_WWW_H
#define FAKE_WWW_H

#define FAKE_WWW_IGNORE_SIZE 1
#define FAKE_WWW_MAX_URL_LEN 2048
#define FAKE_WWW_MIN_CACHE_LEN 1024

struct MemoryStruct {
  char *memory;
  size_t size;
};

typedef struct{
  char **urls;
  int *lengths;
  int nurls;
} fake_www;

void fake_www_init(fake_www* www, char* filename, int flags);
void fake_www_get(fake_www *www, char *url, struct MemoryStruct* chunk);


#endif
