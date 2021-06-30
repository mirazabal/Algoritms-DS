#include "registry.h"
#include <assert.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

typedef struct{
  int64_t i;
  int32_t j;
  int16_t k;
  int8_t l;
} dummy_t;

void push_back_test()
{
  registry_t reg;
  init_registry(&reg, sizeof(dummy_t));

  for(int i =0; i < 512; ++i){
    dummy_t d = {.i = i + 100 };
    push_back_registry(&reg,&d, sizeof(dummy_t));
    test_invariants_registry_hold(&reg);
  }
  free_registry(&reg);
}

void find_registry_test()
{
  registry_t reg;
  init_registry(&reg, sizeof(dummy_t));
  uint32_t keys[512];
  for(int i =0; i < 512; ++i){
    dummy_t d = {.i = i + 100 };
    keys[i] = push_back_registry(&reg,&d, sizeof(dummy_t));
    test_invariants_registry_hold(&reg);
  }
  for(int i = 0; i < 512; ++i){
    void* it = find_registry(&reg, keys[i]);
    assert(it != NULL);
    delete_registry(&reg, keys[i]);
    test_invariants_registry_hold(&reg);
  }
  for(int i = 0; i < 512; ++i){
    void* it = find_registry(&reg, keys[i]);
    assert(it == NULL);
  }
  free_registry(&reg);
}

void free_randomly_test()
{
  const int val = 4096;
  registry_t reg;
  init_registry(&reg, sizeof(dummy_t));
  for(int i =0; i < val; ++i){
    dummy_t d = {.i = i + 100 };
    push_back_registry(&reg,&d, sizeof(dummy_t));
    test_invariants_registry_hold(&reg);
  }

  time_t t;
  srand((unsigned) time(&t));

  for(int i = 0; i < val*4; ++i){
    uint32_t rand_num =rand() % val;
    void* it = find_registry(&reg, rand_num );
    if(it != NULL)
      delete_registry(&reg, rand_num);

    test_invariants_registry_hold(&reg);
  }
  printf("Not deleted items = %ld \n", reg.sz);

  free_registry(&reg);
}

void free_randomly_test_2()
{
  const int val = 5000;
  registry_t reg;
  init_registry(&reg, sizeof(dummy_t));
  for(int i =0; i < val; ++i){
    dummy_t d = {.i = i + 100 };
    push_back_registry(&reg,&d, sizeof(dummy_t));
    test_invariants_registry_hold(&reg);
  }

  time_t t;
  srand((unsigned) time(&t));

  for(int i = 0; i < val*4; ++i){
    uint32_t rand_num =rand() % val;
    void* it = find_registry(&reg, rand_num );
    if(it != NULL)
      delete_registry(&reg, rand_num);

    test_invariants_registry_hold(&reg);
  }

  printf("Not deleted items in test_2 = %ld \n", reg.sz);

  for(int i =0; i < val*5; ++i){
    dummy_t d = {.i = i + 100 };
    push_back_registry(&reg,&d, sizeof(dummy_t));
    test_invariants_registry_hold(&reg);
    if(i%2 == 0){
      uint32_t rand_num = rand() % (5*val);
      void* it = find_registry(&reg, rand_num );
      if(it != NULL)
        delete_registry(&reg, rand_num);

      test_invariants_registry_hold(&reg);
    }
  }

  printf("Not deleted items in test_2 = %ld \n", reg.sz);

  free_registry(&reg);
}




int main()
{
  push_back_test();
  find_registry_test();
  free_randomly_test();
  free_randomly_test_2();
  return EXIT_SUCCESS;
}
