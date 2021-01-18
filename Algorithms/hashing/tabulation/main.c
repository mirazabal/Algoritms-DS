/*
 * Linear hashing implementation directly taken from the paper:
Thorup, Mikkel & Zhang, Yin. (2010). Tabulation Based 5-Universal Hashing and Linear Probing. 
2010 Proceedings of the 12th Workshop on Algorithm Engineering and Experiments,
ALENEX 2010. 62-76. 10.1137/1.9781611972900.7. 
*/

#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>


const int tab_size = 256; // 2exp8
const int num_tab = 16; // 


typedef union{ 
  uint64_t u64; 
  uint32_t u32[2];
  uint16_t u16[4];
  uint8_t u8[8];
} view; 



void gen_rand_tab(uint64_t tab[num_tab][tab_size]) 
{
  time_t t;
  for(int i = 0; i < num_tab; ++i){
    srand((unsigned) time(&t));
    for(int j = 0; j < tab_size; ++j){
      tab[i][j] = rand() % UINT64_MAX; // this is a horrible random function 
    } 
  }
}


// optional compressioninline 
uint64_t compress_c0(uint64_t c0)
{
  const uint64_t Mask1 = 7 +(((uint64_t)7)<<11) + (((uint64_t)7)<<22) +(((uint64_t)7)<<33) + (((uint64_t)7)<<44);
  const uint64_t Mask2 = 255 +(((uint64_t)255)<<11) + (((uint64_t)255)<<22) +(((uint64_t)255)<<33) + (((uint64_t)255)<<44);
  const uint64_t Mask3 = 7 +(((uint64_t)7)<<11) + (((uint64_t)7)<<22) +(((uint64_t)7)<<33) + (((uint64_t)7)<<44);
  return Mask1 + (c0 & Mask2) - ((c0 >> 8) & Mask3);
}
// optional compressioninline
uint32_t compress_c1(uint32_t c1)
{
  const uint64_t Mask1 = (((uint64_t)7)<<11) + 7;const uint64_t Mask2 =(((uint64_t)255)<<11) + 255;
  const uint64_t Mask3 = (((uint64_t)7)<<11) + 7;
  return Mask1 + (c1 & Mask2) - ((c1 >> 8)&Mask3);
}


uint64_t hash(uint64_t key, uint64_t tab[num_tab][tab_size])
{
  view v_key;
  v_key.u64 = key;

  view v0;
  view v1;
  view v2;
  view v3;
  view v4;
  view v5;
  view v6;
  view v7;
  
  v0.u64 = tab[0][v_key.u8[0]]; 
  v1.u64 = tab[1][v_key.u8[1]]; 
  v2.u64 = tab[2][v_key.u8[2]]; 
  v3.u64 = tab[3][v_key.u8[3]]; 
  v4.u64 = tab[4][v_key.u8[4]]; 
  v5.u64 = tab[5][v_key.u8[5]]; 
  v6.u64 = tab[6][v_key.u8[6]]; 
  v7.u64 = tab[7][v_key.u8[7]]; 

  uint64_t c0 = v0.u64 + v1.u64 + v2.u64 + v3.u64 + v4.u64 + v5.u64 + v6.u64 + v7.u64; 
  uint32_t c1 = v0.u32[0] + v1.u32[0] + v2.u32[0] + v3.u32[0] + v4.u32[0] + v5.u32[0] + v6.u32[0] + v7.u32[0]; 
  c0 = compress_c0(c0);
  c1 = compress_c1(c1);

  // I am not completely sure that this works as expected but I followed the paper except for obvious bugs
  return v0.u64 ^ v1.u64 ^ v2.u64 ^ v3.u64 ^ v4.u64 ^ v5.u64 ^ v6.u64 ^ v7.u64 
          ^ tab[8][c0 & 2043] ^ tab[9][(c0>>11) & 2043] ^ tab[10][(c0>>22) & 2043] 
          ^ tab[11][(c0 >> 33)&2043] ^ tab[12][(c0>>44)] ^ tab[13][c1 & 2043] ^ tab[14][(c1>>11)];  
}

int main()
{
  uint64_t tab[num_tab][tab_size];
  gen_rand_tab(tab);

  const int size = 1000000;
  uint64_t keys[size];

  time_t t_rand;
  srand((unsigned) time(&t_rand));
  for(int i = 0; i < size; i++){
    keys[i] = rand() % UINT64_MAX;
  }

  clock_t t; 
  t = clock(); 
  for(int i = 0; i < size; ++i){
    keys[i] = hash(keys[i], tab); 
  }
  t = clock() - t; 
  double time_taken = ((double)t)/CLOCKS_PER_SEC; // in seconds 
  for(int i = 0 ; i < size; ++i){
    printf("key %d = %lu \n", i, keys[i]); 
  }

  printf("fun() took %f seconds to execute \n", time_taken); 

  return 0;
}
