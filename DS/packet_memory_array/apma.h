/*
 * An Adaptative Packed-Memory Array without predictor
 * Implementation from: Michael A. Bender and Haodong Hu. 2007. An adaptive packed-memory array. ACM Trans. Database Syst. 32, 4 (November 2007), 26–es. DOI:https://doi.org/10.1145/1292609.1292616
 */

#include <stdint.h> 

typedef struct key_val_s
{
  int32_t key;
  void* p;
} key_val_t;

typedef struct APMA_s
{
  const int32_t max_occ_h; 
  const int32_t max_occ_0;
  const int32_t min_occ_h;
  const int32_t min_occ_0;
  int64_t last_idx;
  uint32_t cap; // do not change the type since log operation 
  uint32_t size;
  key_val_t* data;
  const uint32_t seg_size; // do not change the type since log operations 
  uint8_t* seg_occ;
//  uint8_t height; // deduce from the amount of segments
} APMA_t;

APMA_t APMA_init(void);

void APMA_free(APMA_t* apma);

int64_t APMA_insert(APMA_t*, key_val_t);

void APMA_delete(APMA_t*, int32_t key);

