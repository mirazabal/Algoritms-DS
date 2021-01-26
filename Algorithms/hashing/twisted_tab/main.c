/*
 * Implementation from: Mihai Pătraşcu and Mikkel Thorup. 2013. Twisted tabulation hashing. In Proceedings of the twenty-fourth annual ACM-SIAM symposium on Discrete algorithms (SODA '13). Society for Industrial and Applied Mathematics, USA, 209–228.
 */

#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>

typedef union{
  uint32_t u32;
  uint16_t u16[2];
  uint8_t u8[4];
} uint32_v;

uint32_t hash_tw(uint32_t x, uint64_t H[4][256])
{
  uint32_v v;
  v.u32 = x;

  uint64_t h = 0;
  for (int i=0; i<3; i++) {
    h^=H[i][v.u8[i]];
  }
  uint8_t c=x^h;              // extra xor with  h
  h^=H[3][c];
  h >>= 32;
  return (uint32_t)h;
}

void gen_tab(uint64_t H[4][256]){
  time_t t;
  for(int i = 0; i < 4; ++i){
    srand((unsigned) time(&t));
    for(int j =0; j < 256; ++j){
      uint64_t rand_1 = rand();
      uint64_t rand_2 = rand();
      H[i][j] = (rand_1 << 31) | rand_2;
    } 
  }
}

int main()
{
  const int size = 1000000;
  uint64_t tab[4][256];
  gen_tab(tab);
  uint32_t keys[size];

  time_t t_rand;
  srand((unsigned) time(&t_rand));
  for(int i = 0; i < size; i++){
    keys[i] = rand(); 
    printf("Gen key  %u \n", keys[i]); 
  }

  clock_t t; 
  t = clock(); 
  for(int i = 0; i < size; ++i){
    keys[i] = hash_tw(keys[i], tab); 
  }
  t = clock() - t; 
  double time_taken = ((double)t)/CLOCKS_PER_SEC; // in seconds 
  for(int i = 0 ; i < size; ++i){
    printf("key %d = %u \n", i, keys[i]); 
  }

  printf("fun() took %f seconds to execute \n", time_taken); 
  return 0;
}

