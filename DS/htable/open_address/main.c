#include "ht.h"
#include <assert.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include "murmur_hash_32.h"


uint32_t hash_func(const void* key_v)
{
  int32_t* key = (int32_t*)key_v;
  static const uint32_t seed = 42;
  return murmur3_32((uint8_t*)key, sizeof(int32_t), seed);
}

bool key_eq_func(const void* a_v, const void* b_v)
{
  int32_t* a = (int32_t*)a_v;
  int32_t* b = (int32_t*)b_v;

  return *a == *b;
}


void free_key_value_func(kv_pair_t* kv)
{
  free((void*)kv->key);
  free(kv->value);
}

int main(){

  htab_t htab;


  init_htab(&htab, hash_func, key_eq_func, free_key_value_func);


  int32_t* key_1 = malloc(sizeof(int));
  int32_t* value_1 = malloc(sizeof(int));
  int32_t* key_2 = malloc(sizeof(int));
  int32_t* value_2 = malloc(sizeof(int));


  *key_1 = 120;
  *value_1 = 500;
  *key_2 = 120;
  *value_2 = 500;

  insert_kv_htab(&htab, key_1, value_1);
  insert_kv_htab(&htab, key_2, value_2);

  int key_3 = 120;
  void* v = find_value_htab(&htab, &key_3);
  assert(v != NULL);
  printf("Value found = %d \n", *((int32_t*)v));

  printf("Size of the hash table = %u num_dirty =%u \n", htab.sz, htab.num_dirty);

  srand (time(NULL));
  for(int i =0; i < 64; ++i){
    int32_t* key_1 = malloc(sizeof(int));
    int32_t* value_1 = malloc(sizeof(int));
    *key_1 = rand() % 128;
    *value_1 = rand() % 128;
    insert_kv_htab(&htab, key_1, value_1);
  }


  printf("Size of the hash table = %u capacity =%u num_dirty = %u \n", htab.sz, htab.cap, htab.num_dirty);

  for(int i =0; i < 256; ++i){
    int key_1 = rand() % 128;
     remove_value_htab(&htab, &key_1);
  }
  
  printf("Size of the hash table = %u capacity =%u num_dirty = %u \n", htab.sz, htab.cap, htab.num_dirty);

  free_htab(&htab);

  return 0;
}

