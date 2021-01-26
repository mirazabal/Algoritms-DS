/*
 * Van Emde Boas tree for uint16_t a la CLRS
 * This version may fail du to the amount of memory requred
 */ 



#include <assert.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdlib.h>

typedef struct vEB_s
{
  uint16_t* max;
  uint16_t* min;
  uint16_t u;

  struct vEB_s* summ;
  struct vEB_s** clstr;
} vEB_t;

uint16_t fsqrt(uint16_t x)
{
  const uint16_t y = x^0xFFFF; //flip bits
  x = x & (y+1); // get the most significant bit 
  return x >> ( __builtin_ctz(x) >> 1); 
}

uint16_t high(vEB_t* t, uint16_t x)
{
  return  x/fsqrt(t->u); 
}

uint16_t low(vEB_t* t,uint16_t x )
{
  return x & (( 1 << (t->u >> 1)) - 1); // x % t->u 
}

uint16_t idx(vEB_t* t, uint16_t x, uint16_t y)
{
  return x*fsqrt(t->u) + y;
}

vEB_t* init_veb(uint64_t u)
{
  assert(u <= UINT16_MAX);
  vEB_t* t = malloc(sizeof(vEB_t));
  assert(t != NULL);
  t->u = u;
  if(u == 2){ 
    t->summ = NULL;
    t->clstr = NULL;
    t->max = NULL;
    t->min = NULL;
    return t;
  }

  t->summ = malloc(sizeof(vEB_t)); 
  assert(t->summ != NULL);

  t->max = NULL; 
  t->min = NULL; 

  const uint16_t num_clstr = fsqrt(u);
  t->clstr = malloc(sizeof(vEB_t*)*num_clstr);

  for(int i = 0; i < num_clstr; ++i){
    t->clstr[i] = init_veb(fsqrt(u)); 
  }
  return t;
}

bool find_veb(vEB_t* t, uint16_t key)
{
  if(key == *t->min || key == *t->max) 
    return true;
  if(t->u == 2) 
    return false;

  return find_veb(t->clstr[high(t,key)], key);
}


int32_t pred_veb(vEB_t* t, uint16_t key)
{
  if(t->u == 2){
    if(key ==1 && *t->min == 0)
      return 0;
    return -1;
  }  
  if(t->max != NULL && *t->max < key){
    return *t->max; 
  }
  uint16_t* min_low = t->clstr[high(t, key)]->min;
  if(min_low != NULL  && low(t,key) > *min_low){
    int32_t offset = pred_veb(t->clstr[high(t,key)], low(t, key)) ; 
    return idx(t, high(t, key), offset); 
  }

  int32_t pred_clstr = pred_veb(t->summ, high(t, key) );
  if(pred_clstr == -1){
    if(t->min != NULL && key > *t->min)
      return *t->min;
    return -1;
  }

  assert(t->clstr[pred_clstr]->max != NULL);
  uint16_t offset = *t->clstr[pred_clstr]->max;
  return idx(t, pred_clstr, offset);
}

int32_t succ_veb(vEB_t* t, uint16_t key)
{
  if(t->u == 2){
    if(key ==0 && *t->max == 1)
      return *t->max; 
    return -1;
  }
  if (t->min != NULL && key < *t->min){
    return *t->min; 
  }
  uint16_t* max_low =  t->clstr[high(t,key)]->max; 
  if(max_low != NULL && low(t,key) < *max_low){
    uint16_t offset = succ_veb(t->clstr[high(t,key) ], low(t,key) );
    return idx(t ,high(t,key),offset);
  }

  int32_t succ_clstr = succ_veb(t->summ, high(t,key) );
  if(succ_clstr == -1) 
    return -1;

  assert(t->clstr[succ_clstr]->min != NULL);
  uint16_t offset = *t->clstr[succ_clstr]->min;
  return idx(t, succ_clstr, offset);
}

static
void insert_empty_tree(vEB_t* t, uint16_t key)
{
  t->max = malloc(sizeof(uint16_t));
  t->min = malloc(sizeof(uint16_t));
  assert(t->max != NULL && t->min != NULL);
  *t->max = key;
  *t->min = key;
}

void insert_veb(vEB_t* t, uint16_t key)
{
  if(t->min == NULL){
    insert_empty_tree(t, key);
    return;
  } 
  if(key < *t->min){
    uint16_t tmp = key;
    key = *t->min;
    *t->min = tmp;
  }

  if(t->u > 2){
    uint16_t* min_val = t->clstr[high(t,key)]->min;
    if(min_val == NULL){
      insert_veb(t->summ, high(t, key)); 
      insert_empty_tree(t->clstr[high(t, key)], low(t, key ));
    }else{
      insert_veb(t->clstr[high(t, key)], low(t, key)); 
    }
  }    
  if(key > *t->max){
    *t->max = key; 
  }
}

void delete_veb(vEB_t* t, uint16_t key)
{
  if(t->min == NULL) return;
  assert(t->max != NULL);
  if(key < *t->min || key > *t->max) return;
  assert(find_veb(t,key) == true); 

  if(*t->max == *t->min == key){
    free(t->max);
    t->max = NULL;
    free(t->min);
    t->min = NULL;
    return;
  }
   
 if(t->u == 2){
    if(key == 0){
      *t->min = 1; 
    } else {
      *t->min = 0; 
    } 
    *t->max = *t->min;
   return;
 }  

 if(key == *t->min){
    uint16_t* first_clstr = t->summ->min; 
    assert(first_clstr != NULL);
    key = idx(t, *first_clstr, *t->clstr[*first_clstr]->min);  
    *t->min = key;
 }

 delete_veb(t->clstr[high(t, key)], low(t, key)); 
  if(t->clstr[high(t, key)]->min == NULL){
    delete_veb(t->summ, high(t,key)); 
    if(key == *t->max){
      uint16_t* summ_max = t->summ->max; 
      if(summ_max == NULL){
        *t->max = *t->min;  
      } else {
        *t->max = idx(t ,*summ_max, *t->clstr[*summ_max]->max); 
      }
    }
  } else if(key == *t->max){
    *t->max = idx(t, high(t, key), *t->clstr[high(t,key)]->max);
  }
}

int main()
{
  vEB_t* t = init_veb(UINT16_MAX);
 
  for(int i = 0; i < 1000; ++i){
    insert_veb(t, i); 
  }

  for(int i = 0; i < 1000; ++i){
    delete_veb(t, i); 
  }


  return 0;
}


