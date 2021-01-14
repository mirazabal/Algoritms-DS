#include "apma.h"
#include <assert.h>
#include <time.h>
#include <stdlib.h>
#include <stdio.h>

int main()
{
  time_t t;
  srand((unsigned) time(&t)); 
  const int val = 1024*128;

  APMA_t apma = APMA_init();
  for (int i = 0; i < val; ++i){
    key_val_t key;
    key.key = rand() % val;
    if(key.key == 0) key.key = 1;
    key.p = malloc(sizeof( int64_t));
    *(int64_t*)key.p = 90 + i;
    APMA_insert(&apma,key); 
    for(int j = 0 ; j < apma.last_idx-1; ++j){
      if (apma.data[j].p != NULL && apma.data[j+1].p != NULL){
        assert(apma.data[j].key <= apma.data[j+1].key); 
      } 
    }
  }
  printf("After insert APMA capacity = %u and size = %u \n ",apma.cap, apma.size);
  for(int i = 0; i < val; i++){
    int key = rand() % val + 1;
    APMA_delete(&apma, key); 
  }
  printf("After delete APMA capacity = %u and size = %u \n ",apma.cap, apma.size);
  APMA_free(&apma);
}
