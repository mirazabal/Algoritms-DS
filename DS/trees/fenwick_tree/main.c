#include "fenwick.h"
#include <stdio.h>

int main()
{
  fwck_t t = fwck_init(128);
  for(int i = 0; i < 100; ++i){
    if(i%2)
      fwck_add(&t, i, 1);
  }
  for(int i = 0; i < 100; i += 3){
    printf("Acc. value = %u for i = %d \n", fwck_acc(&t, 0, i+1),i); 
  }
  fwck_free(&t);
  return 0;
}
