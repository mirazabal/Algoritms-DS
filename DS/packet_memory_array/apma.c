#include "apma.h"

#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define max(a,b) \
   ({ __typeof__ (a) _a = (a); \
       __typeof__ (b) _b = (b); \
     _a > _b ? _a : _b; })

#define min(a,b) \
   ({ __typeof__ (a) _a = (a); \
       __typeof__ (b) _b = (b); \
     _a < _b ? _a : _b; })

static 
bool apma_empty(key_val_t* key)
{
  assert(key != NULL);
  return key->p == NULL;
}

static 
bool apma_not_empty(key_val_t* key)
{
  assert(key != NULL);
  return !apma_empty(key);
}

static
int64_t find_if(key_val_t* arr, int64_t first, int64_t last, bool (*f)(key_val_t*))
{
  assert(arr != NULL);
  assert(f != NULL);
  assert(first <= last);

  while(first!=last){
    if(f(&arr[first])){
      return first;
    } 
    first++;
  }
  return first;
}

static
int64_t find_if_backward(key_val_t* arr, int64_t first, int64_t last, bool (*f)(key_val_t*))
{
  assert(arr != NULL);
  assert(f != NULL);
  assert(first <= last);
  int64_t last_cpy = last; 
  while(last != first){
    if(f(&arr[last-1])){
      return last-1; 
    } 
    --last; 
  }
  return last_cpy;
}

int64_t find_if_bck_fwd(key_val_t* arr, int64_t first, int64_t mid, int64_t last, bool (*f)(key_val_t*))
{
  int64_t idx = find_if_backward(arr, first, mid, f); 
  if(idx != mid) return idx;
  idx = find_if(arr, mid, last, f);
  return idx;
}

int64_t find_if_fwd_bck(key_val_t* arr, int64_t first, int64_t mid, int64_t last, bool (*f)(key_val_t*))
{
  int64_t idx = find_if(arr, mid, last, f);
  if (idx != last) return idx;
  idx = find_if_backward(arr, first, mid, f); 
  return idx;
}

static
int gcd(int a, int b)
{
  while(b != 0){
    int t = a % b;
    a = b;
    b = t;
  } 
  return a;
}

static
void rotate_cycle(key_val_t* arr, int64_t first, int64_t last, int64_t initial, int64_t shift)
{
  key_val_t value = arr[initial];
  int64_t idx_1 = initial; 
  int64_t idx_2 = idx_1 + shift;

  while(idx_2 != initial){
    arr[idx_1] = arr[idx_2];
    idx_1 = idx_2;
    if(last - idx_2 > shift)
      idx_2 += shift;
    else
      idx_2 = first + (shift - (last - idx_2));
  }
  arr[idx_1] = value;
}

static
void rotate(key_val_t* arr, int64_t first, int64_t middle, int64_t last)
{
  if(first == middle || middle == last) return;
  int distance = gcd(last-first, middle-first);
  while(distance--){
    rotate_cycle(arr, first, last, first + distance, middle-first); 
  }
}

static 
int64_t stable_partition(key_val_t* arr, int64_t first, int64_t last, bool(*f)( key_val_t*))
{
  int64_t len = last - first;
  assert(len>0);
  if(len == 1) return f(&arr[first]) ? last : first;

  int64_t middle = first + len/2;
  int64_t first_cut = stable_partition(arr, first, middle, f);
  int64_t second_cut = stable_partition(arr,  middle, last, f);

  rotate(arr, first_cut, middle, second_cut);
  return first_cut + (second_cut - middle);
}

static 
int64_t lower_bound(APMA_t* apma, int64_t first_idx, int64_t last_idx, int32_t key)
{
  first_idx = find_if(apma->data, first_idx, last_idx, apma_not_empty);
  if(first_idx == last_idx) return last_idx;

  int len = last_idx - first_idx;
  while(len>0){
    int mid_idx = first_idx;
    int step = len/2;
    mid_idx = mid_idx + step;
    int mid_idx_view = mid_idx;
    if(apma->data[mid_idx].p == NULL){
      mid_idx_view = find_if_bck_fwd(apma->data, first_idx, mid_idx, first_idx + len, apma_not_empty); 
      if(mid_idx_view == first_idx+len) return first_idx;
    }
    if(apma->data[mid_idx_view].key < key){
      len = len - (max(mid_idx_view, mid_idx) + 1 - first_idx);
      first_idx = max(mid_idx_view, mid_idx) + 1;
    } else if(apma->data[mid_idx_view].key > key){
      len = mid_idx_view - first_idx;
    } else { // apma->data[mid_idx_view].key == key
      if(mid_idx_view > mid_idx){ // no slot between first_idx and mid_idx
        len = len - (mid_idx - first_idx) -1;
        first_idx = mid_idx+1; 
      } else if (mid_idx_view == first_idx || mid_idx_view == first_idx + 1){
        return mid_idx_view;
      } else {
        len = mid_idx_view - first_idx + 1;
      }
    }
  }
  assert(first_idx <= last_idx);
  return first_idx;
}

static
int64_t upper_bound(APMA_t* apma, uint64_t first_idx, uint64_t last_idx, key_val_t* key_val)
{
  assert(first_idx <= last_idx);
  int64_t len = last_idx - first_idx;
  while(len>0){
    const int64_t half = len >> 1;
    int64_t mid_idx = first_idx + half;
    int mid_idx_view = mid_idx;
    if(apma->data[mid_idx].p == NULL){
      mid_idx_view = find_if_bck_fwd(apma->data, first_idx, mid_idx, first_idx + len, apma_not_empty);
      if(mid_idx_view == first_idx + len) return first_idx;
    } 
    if(key_val->key < apma->data[mid_idx_view].key){
      if(mid_idx_view > mid_idx) 
        return first_idx;
      len = mid_idx_view - first_idx;
    } else {
      len = len - (mid_idx_view + 1 - first_idx);
      first_idx = mid_idx_view + 1;
    }
  }
  assert(first_idx <= last_idx);
  return first_idx;
}

static
uint32_t accumulate(uint8_t* arr, uint32_t first, uint32_t last, uint32_t start)
{
  assert (arr != NULL);
  while(first != last){
    start += arr[first];
    ++first;
  }
  return start;
}

static
uint32_t count_if(key_val_t* arr, uint32_t first, uint32_t last, bool(*f)(key_val_t*))
{
  uint32_t val = 0;
  while(first != last)
  {
    if(f(&arr[first]))
      val += 1;
    ++first; 
  }
  return val;
}

static 
void swap(key_val_t** a, key_val_t** b)
{
  key_val_t* tmp = *a;
  *a = *b;
  *b = tmp;
}

static
bool max_num_elem_limit(APMA_t* apma, int left_idx_start, int right_idx_start, int right_idx_end)
{
  int elem_left = count_if(apma->data, left_idx_start,  right_idx_start, apma_not_empty);
  int elem_right = count_if(apma->data, right_idx_start, right_idx_end, apma_not_empty);
  return  elem_left <7 && elem_right < 7;
}

// TODO: find the minimum # of memcpy..  
static
void sparse(APMA_t* apma, int32_t insert_idx, int32_t lev)
{
  if(lev == 0) return;
  
  insert_idx = min(insert_idx, apma->cap -1);

  const uint32_t seg_idx = insert_idx/(uint32_t)apma->seg_size & (~0U << lev); // clear last n bits 

  const int left_idx_start = seg_idx*apma->seg_size;
  const int left_idx_end = left_idx_start + (1 <<  (lev - 1) )*apma->seg_size;
  const int left_elem = count_if(apma->data, left_idx_start, left_idx_end, apma_not_empty);

  const int right_idx_start = left_idx_end;
  const int right_idx_end = right_idx_start + (1 << (lev -1))*apma->seg_size; 
  const int right_elem = count_if(apma->data, right_idx_start, right_idx_end, apma_not_empty);

  const int excess = left_elem - ((left_elem + right_elem) >> 1);    
  if(excess == 0) {
    goto divide_tree;
  }

  bool (*f)(key_val_t*) = excess > 0 ?  apma_empty : apma_not_empty;
  bool (*not_f)(key_val_t*) = excess > 0 ?  apma_not_empty : apma_empty;

  int64_t idx_l = left_idx_end - abs(excess);// if left_elem == 0  
  if(left_elem != 0){
    int idx = left_idx_end;
    for(int i = 0 ; i < abs(excess); ++i){
      idx = find_if_backward(apma->data, left_idx_start, idx, not_f);
    } 
    idx_l = stable_partition(apma->data, idx, left_idx_end, f); 
  }
 
  //int64_t idx_r = right_idx_end - abs(excess); 
  if(right_elem != 0){
    int idx = right_idx_start;
    for(int i = 0; i < abs(excess); ++i){
      idx = find_if(apma->data, idx, right_idx_end, f);
      if (idx != right_idx_end)
        idx += 1;
    } 
    //idx_r = stable_partition(apma->data, right_idx_start, idx, f);
    stable_partition(apma->data, right_idx_start, idx, f);
  }

  const int64_t src = excess > 0 ? idx_l : right_idx_start;
  const int64_t dest = excess > 0 ? right_idx_start : idx_l;
  memcpy(&apma->data[dest], &apma->data[src], sizeof(apma->data[0])*abs(excess));
  memset(&apma->data[src], 0, sizeof(apma->data[0])*abs(excess));

  if(lev ==1){
    assert(max_num_elem_limit(apma, left_idx_start, right_idx_start, right_idx_end));
  }

divide_tree:
  sparse(apma, left_idx_start, lev-1);
  sparse(apma, right_idx_start, lev-1);
}

static
bool size_eq_occ(APMA_t* apma)
{
  uint32_t seg_occ = accumulate(apma->seg_occ, 0, apma->cap / apma->seg_size, 0);
  if(seg_occ != apma->size)
    printf("seg_occ = %u and apma->size == %d", seg_occ, apma->size);
  return seg_occ == apma->size;
}

__attribute__((no_sanitize("memory")))
static void shift_left(void* src, size_t elem, int pos, size_t n) {
  void* dest = src - pos*n;
  memcpy(dest, src, elem*n);
  memset(dest+elem*n, 0, pos*n);
}

__attribute__((no_sanitize ("memory")))
static void shift_right(void* src, size_t elem, int pos, size_t n)
{
  void* dest = src + pos*n;
  memcpy(dest,src, elem*n);
  memset(src, 0, pos*n);
}

static
void insert_at_idx(APMA_t* apma, key_val_t* key_val, int64_t insert_idx)
{
  assert(size_eq_occ(apma));
  const int64_t start_seg = min( (insert_idx/apma->seg_size)* apma->seg_size, apma->cap - apma->seg_size);
  const int64_t end_seg = min( (insert_idx/apma->seg_size + 1)* apma->seg_size, apma->cap); // case when insert_idx == apma->cap

  const int64_t empty_idx = find_if_fwd_bck(apma->data, start_seg, insert_idx, end_seg, apma_empty); 
  if(empty_idx != insert_idx){
    if (empty_idx > insert_idx){
      shift_right( &apma->data[insert_idx], empty_idx - insert_idx, 1, sizeof(key_val_t));
    } else {
      shift_left(&apma->data[empty_idx+1], insert_idx - empty_idx -1 , 1, sizeof(key_val_t));
      insert_idx = insert_idx - 1;
    } 
  }
  assert(apma->data[insert_idx].p == NULL);
  assert(insert_idx < apma->cap);

  apma->data[insert_idx] = *key_val;

  assert(empty_idx <= apma->last_idx);
  if (empty_idx == apma->last_idx)
      ++apma->last_idx;

  assert(size_eq_occ(apma));
  assert(apma->seg_occ[insert_idx/apma->seg_size] < 7);
  apma->seg_occ[insert_idx/apma->seg_size]++;
  apma->size++;
  assert(size_eq_occ(apma));

  if(insert_idx > 0 && apma->data[insert_idx-1].p != NULL){
    assert(apma->data[insert_idx-1].key <= apma->data[insert_idx].key);
  }
  if(insert_idx < end_seg -  1 && apma->data[insert_idx+1].p != NULL){
    assert(apma->data[insert_idx].key <= apma->data[insert_idx+1].key); 
  }
}

static
int32_t max_occ_level(APMA_t* apma, float tree_lev, int lev)
{
  assert(!(tree_lev < lev));
  if(tree_lev == 0) return apma->max_occ_0;
  const float incr = (float)(apma->max_occ_0 - apma->max_occ_h)/(tree_lev); 
  return apma->max_occ_0 - lev*incr; 
}

static
int max_threshold_surpassed(APMA_t* apma, int tree_lev, int64_t insert_idx)
{
  assert(tree_lev > -1);
  assert(insert_idx > -1);
  assert(apma != NULL);
  assert(apma->max_occ_0 >= apma->max_occ_h);
  int lev = 0;
  int largest_lev = -1;
  while (lev < tree_lev + 1){
    const int32_t max_occ = max_occ_level(apma, tree_lev, lev);
    const uint32_t first_seg_idx = insert_idx/(uint32_t)apma->seg_size & (~0U << lev);
    const uint32_t last_seg_idx = first_seg_idx + (1U << lev); 
    const int32_t max_elem = max_occ * (last_seg_idx - first_seg_idx); 
    const uint32_t window_occ = accumulate(apma->seg_occ, first_seg_idx, last_seg_idx, 0); 
    if (window_occ >=  max_elem)
        largest_lev = lev; 
    ++lev;
  }

  assert(tree_lev >= largest_lev);
  return largest_lev; 
}

static
int32_t min_occ_level(APMA_t* apma, float tree_lev, int lev)
{
  assert(!(tree_lev < lev));
  assert(apma->min_occ_h >= apma->min_occ_0);
  if(tree_lev == 0) return apma->min_occ_0;
  const float incr = (float)(apma->min_occ_h - apma->min_occ_0)/(tree_lev); 
  return apma->min_occ_0 + lev*incr; 
}

static
int min_threshold_surpassed(APMA_t* apma, int tree_lev, int64_t insert_idx)
{
  assert(tree_lev > -1);
  assert(insert_idx > -1);
  assert(apma != NULL);
  int lev = 0;
  int largest_lev = -1;
  while (lev < tree_lev + 1){
    const int32_t min_occ = min_occ_level(apma, tree_lev, lev);
    const uint32_t first_seg_idx = insert_idx/(uint32_t)apma->seg_size & (~0U << lev);
    const uint32_t last_seg_idx = first_seg_idx + (1U << lev); 
    const uint32_t window_occ = accumulate(apma->seg_occ, first_seg_idx, last_seg_idx , 0); 
    const int32_t min_elem = min_occ * (last_seg_idx - first_seg_idx);
    if (window_occ <= min_elem)
        largest_lev = lev; 
    ++lev;
  }
  return largest_lev; 
}

static
void evenly_cpy(APMA_t* apma, key_val_t* dest, uint32_t seg_start_idx)
{
  const int start_idx = seg_start_idx*apma->seg_size;
  const int last_idx = (seg_start_idx+1) *apma->seg_size;
  int idx  = start_idx;
  for(int i = 0; i < apma->seg_occ[seg_start_idx]/2; i++){
    idx = find_if(apma->data, idx, last_idx, apma_not_empty); 
    idx = idx + 1;
  }
  memcpy(&dest[seg_start_idx*2*apma->seg_size],&apma->data[start_idx], (idx - start_idx)*(sizeof(key_val_t)));
  memcpy(&dest[((seg_start_idx*2)+1)*apma->seg_size],&apma->data[idx], (last_idx - idx) *(sizeof(key_val_t)));

}

static
void resize_insert(APMA_t* apma, key_val_t* key_val)
{
  assert(apma != NULL);
  key_val_t* tmp = calloc(2*apma->cap, sizeof(key_val_t));
  for(int i = 0; i < apma->cap/apma->seg_size; ++i){
    evenly_cpy(apma, tmp, i); 
  }
  free(apma->data);
  swap(&tmp,&apma->data); 
  apma->cap = 2*apma->cap;
  free(apma->seg_occ);
  apma->seg_occ = calloc(apma->cap/apma->seg_size, sizeof(apma->seg_occ[0]));
}

void evenly_cpy_del(APMA_t* apma, key_val_t* tmp)
{
   const int32_t num_slots = (apma->cap/apma->seg_size); 
   int32_t per_slot = apma->size/num_slots;   
   int32_t q = apma->size % num_slots;
   const int32_t dense_slot = 2*per_slot; 
   int32_t start_src_idx = 0;
   for(int i = 0; i < num_slots/2; ++i){
      int32_t elem = dense_slot;
      if(q > 0){
        elem = elem +1;
        q = q - 1;
      }
      int32_t dest_idx = i*apma->seg_size;
      while(elem != 0){
        start_src_idx = find_if(apma->data, start_src_idx, apma->last_idx, apma_not_empty);  
        tmp[dest_idx] = apma->data[start_src_idx];
        dest_idx = dest_idx + 1;
        start_src_idx = start_src_idx + 1;  
        elem = elem - 1; 
      }
   }
}

static
void resize_delete(APMA_t* apma, int32_t idx)
{
  assert(apma != NULL);
  assert(idx > -1);
 
  if(apma->cap == apma->seg_size) return;

  key_val_t* tmp = calloc(apma->cap /2, sizeof(key_val_t));
  evenly_cpy_del(apma, tmp);

  free(apma->data);
  swap(&tmp, &apma->data);
  apma->cap = apma->cap/2;
  free(apma->seg_occ);
  apma->seg_occ = calloc(apma->cap/apma->seg_size, sizeof(apma->seg_occ[0]));
}

APMA_t APMA_init(void)
{
  APMA_t apma = {.max_occ_h = 6, .max_occ_0 = 7, .min_occ_h = 3, .min_occ_0 = 2, .cap = 0, .size = 0,  .last_idx=0   ,.seg_size = 8};  

  apma.seg_occ = malloc(sizeof(uint8_t));
  assert(apma.seg_occ != NULL);
  *apma.seg_occ = 0;

  apma.data = malloc(sizeof(key_val_t) * apma.seg_size);
  assert(apma.data != NULL);
  // memset should work on most platforms
  for (int i =0; i < apma.seg_size; ++i){
    apma.data[i].p = NULL; 
  } 
  apma.cap = apma.seg_size;
  return apma;
}

void APMA_free(APMA_t* apma)
{
  for(int i =0; i < apma->last_idx; ++i){
    if(apma->data[i].p != NULL)
      free(apma->data[i].p); 
  }
  free(apma->data);
  free(apma->seg_occ);
}

static
bool all_seg_occ_above(APMA_t* apma, int val)
{
  for(int i = 0; i < apma->cap/apma->seg_size; ++i){
      int count = count_if(apma->data, i*apma->seg_size, (i+1)*apma->seg_size, apma_not_empty); 
      if(count < val && apma->cap > apma->seg_size)
        return false;
  }
  return true;
}

static
bool all_seg_occ_below(APMA_t* apma, int val)
{
  for(int i = 0; i < apma->cap/apma->seg_size; ++i){
      int count = count_if(apma->data, i*apma->seg_size, (i+1)*apma->seg_size, apma_not_empty); 
      if(count >= val && apma->cap > apma->seg_size)
        return false;
  }
  return true;
}

static
bool APMA_invariants(APMA_t* apma)
{
  assert(all_seg_occ_below(apma, apma->max_occ_0 + 1));
  assert(all_seg_occ_above(apma, apma->min_occ_h - 1));
  assert(size_eq_occ(apma));
  return true;
}

int64_t APMA_insert(APMA_t* apma, key_val_t key_val)
{
  assert(apma != NULL);
  assert(key_val.key != 0 && "Zero is not a permitted value");
  assert(APMA_invariants(apma));

  int64_t insert_idx = upper_bound(apma, 0, apma->last_idx, &key_val);
  const int tree_lev = 31 - __builtin_clz(apma->cap/apma->seg_size); // log base 2
  const int lev_sur = max_threshold_surpassed(apma, tree_lev, min(insert_idx, apma->cap-1)); 
  if(lev_sur != -1){
    if(lev_sur == tree_lev){ 
      resize_insert(apma, &key_val);
    } else {
      sparse(apma, insert_idx, lev_sur+1);
    }
    for(int i = 0; i < apma->cap/apma->seg_size; ++i){
      apma->seg_occ[i] = count_if(apma->data, i*apma->seg_size, (i+1)*apma->seg_size, apma_not_empty); 
    }
    apma->last_idx = find_if_backward(apma->data, 0, apma->cap, apma_not_empty);
    apma->last_idx = min(apma->last_idx + 1, apma->cap);
    insert_idx = upper_bound(apma, 0,  apma->cap, &key_val);
    assert(insert_idx <= apma->last_idx);
  }
  assert(APMA_invariants(apma));
  insert_at_idx(apma, &key_val, insert_idx);
  assert(APMA_invariants(apma));
  return insert_idx; 
}

void APMA_delete(APMA_t* apma, int32_t key)
{
  assert(key != 0 && "Zero is not a permitted value");
  assert(APMA_invariants(apma));
  
  int64_t idx = lower_bound(apma, 0, apma->last_idx , key);
  if(apma->data[idx].key != key){
    return;
  }
  assert(apma->data[idx].p != NULL);
  free(apma->data[idx].p);
  apma->data[idx].p = NULL;
  apma->data[idx].key = 0;
  apma->seg_occ[idx/apma->seg_size] = apma->seg_occ[idx/apma->seg_size]  - 1;
  assert(apma->size > 0);
  apma->size = apma->size - 1;

  const int tree_lev = 31 - __builtin_clz(apma->cap/apma->seg_size); // log base 2
  const int lev_sur = min_threshold_surpassed(apma, tree_lev, idx); 
  if(lev_sur != -1){
    if(lev_sur == tree_lev){
      resize_delete(apma, idx); 
    } else {
      sparse(apma, idx, lev_sur+1);
    } 
    for(int i = 0; i < apma->cap/apma->seg_size; ++i){
      apma->seg_occ[i] = count_if(apma->data, i*apma->seg_size, (i+1)*apma->seg_size, apma_not_empty); 
    }
    apma->last_idx = find_if_backward(apma->data, 0, apma->cap, apma_not_empty);
    if (apma->last_idx == apma->cap){ // the array is empty
      apma->last_idx = 0; 
    }else {
      apma->last_idx = apma->last_idx + 1; 
    }
  }
  assert(APMA_invariants(apma));
}

