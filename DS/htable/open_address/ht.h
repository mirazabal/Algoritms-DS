#ifndef HASH_TABLE_OPEN_ADDRESSING_NAIVE_H
#define HASH_TABLE_OPEN_ADDRESSING_NAIVE_H


#include <stdint.h>
#include <stdbool.h>


typedef struct{
  const void* key;
  void* value;
} kv_pair_t;

typedef struct{
  kv_pair_t kv;
  uint32_t hash;
  bool is_dirty;
  bool has_value;
} hentry_t;


typedef uint32_t (*hash_func_fp)(const void* key);

typedef bool (*key_eq_func_fp)(const void* a, const void* b);

typedef void (*free_key_value_func_fp)(kv_pair_t* kv);


typedef struct {
  hentry_t* arr;

  uint32_t sz;
  uint32_t cap;
  // # of used entries, even if they are now freed
  uint32_t num_dirty; 
  hash_func_fp hf;
  key_eq_func_fp key_eq;
  free_key_value_func_fp free_kv;
} htab_t;


void init_htab(htab_t* htab, hash_func_fp hf, key_eq_func_fp key_eq, free_key_value_func_fp);

void free_htab(htab_t* htab);

void insert_kv_htab(htab_t* htab, const void* key, void* value);

void remove_value_htab(htab_t* htab, const void* key); 

void* find_value_htab(htab_t* htab, const void* key);

#endif

