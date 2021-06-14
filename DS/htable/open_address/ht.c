#include "ht.h"

#include <assert.h>
#include <stddef.h>
#include <stdlib.h>

static 
const int MIN_SIZE_HT = 16;

void init_htab(htab_t* htab, hash_func_fp hf, key_eq_func_fp key_eq, free_key_value_func_fp free_kv)
{
  assert(htab != NULL);
  assert(hf != NULL);
  assert(key_eq != NULL);

  htab->arr = calloc(MIN_SIZE_HT, sizeof(hentry_t));
  assert(htab->arr != NULL);
  htab->cap = MIN_SIZE_HT;
  htab->sz = 0;
  htab->num_dirty = 0;

  htab->hf = hf;
  htab->key_eq = key_eq;
  htab->free_kv = free_kv;
}

void free_htab(htab_t* htab)
{
  assert(htab != NULL);

  if(htab->free_kv != NULL){
    for(int i = 0; i < htab->cap; ++i){
      if(htab->arr[i].has_value == true){
        assert(htab->arr[i].is_dirty);
        htab->free_kv(&htab->arr[i].kv);
      }
    }
  }
  free(htab->arr);
}

static
uint32_t find_idx(htab_t* htab, const void* key, uint32_t hash)
{
  const uint32_t start_idx = hash % htab->cap;
  uint32_t idx = start_idx;
  do{
    const hentry_t* entry = &htab->arr[idx];
    if(entry->is_dirty == false)
      return idx;

    if(entry->has_value == true && htab->key_eq(key, entry->kv.key) == true){
      return idx;
    }

    idx += 1;
    if(idx == htab->cap)
      idx = 0;
  } while(start_idx != idx);

  assert(0!=0 && "Impossible code path. There must be a free entry.");
}

static
void rehash_table(htab_t* htab, uint32_t cap)
{
  assert(htab != NULL);

  htab_t old_htab = *htab;

  hentry_t* new_arr = calloc(cap, sizeof(hentry_t)); 
  assert(new_arr != NULL);

  htab->cap = cap;
  htab->arr = new_arr;
  htab->num_dirty = 0;

  for(size_t idx_old = 0; idx_old < old_htab.cap; ++idx_old ){
    if(old_htab.arr[idx_old].has_value == true){
      assert(old_htab.arr[idx_old].is_dirty == true);
      const uint32_t hash = old_htab.arr[idx_old].hash;
      const void* key = old_htab.arr[idx_old].kv.key;
      const uint32_t idx_new = find_idx(htab, key, hash); 
      htab->arr[idx_new] = old_htab.arr[idx_old];
      htab->num_dirty += 1;
    }
  }
  free(old_htab.arr);
}

static
void expand_or_shrink_if_neccesary(htab_t* htab)
{
  if(htab->num_dirty * 2 > htab->cap){
      rehash_table(htab, htab->cap * 2);
  } else if (htab->sz * 4 < htab->cap && htab->cap > MIN_SIZE_HT){
      rehash_table(htab, htab->cap/2);
  } 
  assert(htab->sz * 2 <= htab->cap);
  assert(htab->num_dirty * 2 <= htab->cap);
}

void insert_kv_htab(htab_t* htab, const void* key, void* value)
{
  expand_or_shrink_if_neccesary(htab);
  assert(htab->num_dirty * 2 <= htab->cap );

  const uint32_t hash = htab->hf(key);
  const uint32_t idx = find_idx(htab, key, hash);
  assert(idx < htab->cap); 

  hentry_t* entry = &htab->arr[idx];
  if(entry->has_value == true){
    assert(entry->is_dirty == true);
    htab->free_kv(&entry->kv);
  } else
    htab->sz += 1;

  entry->kv.key = key;
  entry->kv.value = value;
  entry->hash = hash;
  if(entry->is_dirty == false)
    htab->num_dirty += 1;
  entry->is_dirty = true;
  entry->has_value = true;

}

static
hentry_t* find_entry(htab_t* htab, const void* key)
{
  const uint32_t hash = htab->hf(key);
  const uint32_t start_idx = hash % htab->cap;
  uint32_t idx = start_idx;

  do{
    hentry_t* entry = &htab->arr[idx];
    if(entry->is_dirty == false){
      assert(entry->has_value == false);
      return NULL;
    }
    if(entry->has_value && htab->key_eq(key, entry->kv.key) == true){
      return entry;
    }
    idx += 1;
    if(idx == htab->cap)
      idx = 0;

  } while(idx != start_idx);

  assert(0!=0 && "Impossible code path. There must be a free entry.");
}

void remove_value_htab(htab_t* htab, const void* key)
{
  expand_or_shrink_if_neccesary(htab);
  assert(htab->num_dirty * 2 <= htab->cap );

  hentry_t* entry = find_entry(htab, key);
  if(entry == NULL) return;

  assert(entry->is_dirty == true && entry->has_value == true);
   
  htab->free_kv(&entry->kv);
  entry->has_value = false;
  htab->sz -=1;
}

void* find_value_htab(htab_t* htab, const void* key)
{
  assert(htab != NULL);
  assert(key != NULL);
  hentry_t* entry = find_entry(htab, key); 

  return entry != NULL ? &entry->kv.value : NULL;
}

