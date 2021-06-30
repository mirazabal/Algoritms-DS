#include <assert.h>
#include <stdlib.h>
#include <string.h>
#include "registry.h"

static
const int MIN_SIZE = 16;

typedef struct{
  uint32_t key;
  bool has_value;
  // Do NOT change the order in which the variables are declared in the struct
  // as val is an incomplete array type
  uint8_t val[];
} registry_bucket_t ;

static inline
size_t bucket_sz(registry_t* reg)
{
  return sizeof(registry_bucket_t) + sizeof( uint8_t[ reg->elm_sz] );
}

static inline
bool has_value_buckets(void* b_v)
{
  registry_bucket_t* b = (registry_bucket_t* )b_v; 
  return b->has_value;
}

static
size_t lower_bound(void* bucket, size_t sz, uint32_t key, size_t b_size)
{
  assert(sizeof(registry_bucket_t) < b_size && "Registry bucket has an incomplete array type, val, and thus it must be larger");
  size_t lower = 0;
  int len = sz;
  size_t idx = 0;
  while(len > 0){
    int half = len/2;
    idx = lower + half;
    registry_bucket_t* b = bucket + idx*b_size;
    if(b->key < key){
      lower = idx+1;
      len = len - half -1;
    } else {
      len = half;
    }
  }
  return lower; 
}

static
size_t copy_if(size_t elm_sz, void* it_start, size_t n_memb, void* it_output, bool (*fp)(void*))
{
  assert(it_start != NULL);
  assert(it_output != NULL);

  size_t i = 0;
  size_t i_out = 0;
  while(i < n_memb){
    if(fp(it_start + i*elm_sz) == true){
       memcpy(it_output + elm_sz*i_out, it_start+i*elm_sz, elm_sz);
       ++i_out;
    }
    ++i;
  }
  return i_out;
}

static 
size_t partition(size_t elm_sz, void* it_start, size_t n_memb, bool (*fp)(void*))
{
  assert(it_start != NULL);
  size_t i = 0;
  size_t j = 0;
  while(i < n_memb){
    if(fp(it_start + elm_sz*i)){
      memmove(it_start + elm_sz*j, it_start+elm_sz*i, elm_sz);
      ++j;
    }
    ++i;
  }
  return j; 
}

static
void shrink_if_necessary(registry_t* reg)
{
  if(reg->cap == MIN_SIZE || reg->sz*4 > reg->cap )
    return;

  const size_t b_size = bucket_sz(reg);
  const size_t idx = partition(b_size, reg->arr, reg->occ_bucket, has_value_buckets);
  assert(idx <= reg->occ_bucket);

  memset( reg->arr + b_size*idx , 0, (reg->cap - idx)* b_size);

  registry_bucket_t* tmp = calloc(reg->cap/2, b_size);
  assert(tmp != NULL);
  memcpy(tmp, reg->arr, idx*b_size);

  free(reg->arr);
  reg->arr = tmp;
  reg->occ_bucket = idx;
  reg->cap = reg->cap/2;
}

static
void compact_if_necessary(registry_t* reg)
{
  if(reg->sz * 2 > reg->occ_bucket)
    return;

  const size_t b_size = bucket_sz(reg);
  const size_t idx = partition(b_size, reg->arr, reg->occ_bucket, has_value_buckets);
  assert(idx < reg->occ_bucket);

  memset( reg->arr + b_size*idx , 0, (reg->cap - idx)* b_size);

  reg->occ_bucket = idx;
}

static
void expand_if_neccesary(registry_t* reg)
{
  assert(reg != NULL);
  if(reg->occ_bucket < reg->cap)
    return;

  const size_t b_size = bucket_sz(reg);
  registry_bucket_t* tmp_arr = calloc(reg->cap*2, b_size);
  assert(tmp_arr != NULL);
  
  const size_t out_idx = copy_if( b_size, reg->arr, reg->occ_bucket , tmp_arr, has_value_buckets);

  free(reg->arr);

  reg->arr = tmp_arr;
  reg->occ_bucket = out_idx;
  reg->cap = reg->cap*2;
}

void init_registry(registry_t* reg, size_t elm_sz)
{
  assert(reg != NULL);

  reg->sz = 0;
  reg->cap = MIN_SIZE; 
  reg->elm_sz = elm_sz;
  reg->occ_bucket = 0;
  reg->key_id = 0;

  // http://www.open-std.org/jtc1/sc22/wg14/www/docs/n1548.pdf
  // From C11 draft, page 112
  // A structure or union shall not contain a member with incomplete 
  // or function type (hence,a structure shall not contain an instance of 
  // itself, but may contain a pointer to an instanceof  itself),  except  
  // that  the  last  member  of  a  structure  with  more  than  one  named  
  // member may  have  incomplete  array  type;  such  a  structure  (and  any  
  // union  containing,  possibly recursively, a member that is such a 
  // structure) shall not be a member of a structure or anelement of an array.
   
  //EXAMPLE 2 @ page 114 of C11 draft: After the declaration:
  //struct s { int n; double d[]; };
  //the structure struct s has a flexible array member d. A typical way to use 
  //this is:
  //int m = /*some value*/;
  //struct s *p = malloc(sizeof (struct s) + sizeof (double [m]));
  //and assuming that the call to malloc succeeds, the object pointed to 
  //by p behaves, for most purposes, as if p had been declared as:
  //struct { int n; double d[m]; } *p;
 
  const size_t b_size = bucket_sz(reg);
  reg->arr = calloc( MIN_SIZE, b_size); //  
  assert(reg->arr != NULL);

  }

void free_registry(registry_t* reg)
{
  assert(reg != NULL);
  free(reg->arr);
}

void* find_registry(registry_t* reg, uint32_t key)
{
  const size_t b_size = bucket_sz(reg);
  const uint32_t idx = lower_bound(reg->arr, reg->occ_bucket, key, b_size); 
  assert(idx <= reg->occ_bucket);

  if(idx == reg->occ_bucket)
    return NULL;

  registry_bucket_t* b = reg->arr + b_size*idx;
  if(b->has_value == false || b->key != key)
    return NULL;

  return b->val;
}

uint32_t push_back_registry(registry_t* reg, void* value, size_t elm_sz)
{
  assert(reg != NULL);
  assert(elm_sz == reg->elm_sz);

  expand_if_neccesary(reg);

  const size_t b_size = bucket_sz(reg);
  registry_bucket_t* b = reg->arr + b_size* reg->occ_bucket;

  memcpy(b->val, value, elm_sz);
  const uint32_t key = reg->key_id;
  b->key = key;
  b->has_value = true;

  assert(reg->key_id != SIZE_MAX && "Overflow reached!");

  ++reg->key_id;
  ++reg->occ_bucket;
  ++reg->sz;

  return key;
}

void delete_registry(registry_t* reg, uint32_t key)
{
  assert(reg != NULL);

  const size_t b_size = bucket_sz(reg);
  const uint32_t idx = lower_bound(reg->arr, reg->occ_bucket , key, b_size);   

  assert(idx < reg->occ_bucket);

  registry_bucket_t* b = reg->arr + b_size*idx;

  assert(b->has_value == true && b->key == key);
 
   --reg->sz;
   b->has_value = false; 

  compact_if_necessary(reg);
  shrink_if_necessary(reg);
}

void test_invariants_registry_hold(registry_t* reg)
{
  assert(reg != NULL);
  assert(reg->cap >= reg->occ_bucket);
  assert(reg->cap >= reg->sz);
 
  const size_t b_size = bucket_sz(reg);

  uint32_t counter = 0;
  int64_t last_key = -1;
  // Test monotonic order
  for(int i =0; i < reg->occ_bucket; ++i){
    registry_bucket_t* b = reg->arr + b_size*i;
    if(b->has_value)
      ++counter;
    assert(b->key > last_key);
    last_key = b->key;
  }
  assert(counter == reg->sz);
}

