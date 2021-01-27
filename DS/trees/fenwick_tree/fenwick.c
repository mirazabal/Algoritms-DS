#include "fenwick.h"

#include <assert.h>
#include <stdlib.h>

uint32_t lsb(uint32_t x)
{
  return x & (~x +1); // x AND x's 2's complement 
}

fwck_t fwck_init(uint32_t size)
{
  fwck_t t;
  t.p = calloc(size, sizeof(uint32_t));
  t.size = size;
  return t;
}

void fwck_free(fwck_t* t)
{
  free(t->p);
}

void fwck_add(fwck_t* t, uint32_t pos, uint32_t delta)
{
  assert(t != NULL);
  assert(pos < t->size);
  pos++;
  while(pos <= t->size){
    assert(t->p[pos-1] + delta >= t->p[pos-1]); // overflow check
    t->p[pos-1] += delta;
    pos += lsb(pos);   
  }
}

void fwck_del(fwck_t* t, uint32_t pos, uint32_t delta)
{
  assert(t != NULL);
  assert(pos < t->size);
  pos++;
  while(pos <= t->size){
    assert(t->p[pos-1] - delta <= t->p[pos-1]); // overflow check
    t->p[pos-1] -= delta;
    pos += lsb(pos);   
  }
}

uint32_t fwck_acc(fwck_t* t, uint32_t first, uint32_t last)
{
  assert(first <= last);
  uint32_t sum = 0;
  while(last > first){
    assert(sum + t->p[last-1] >= sum);
    sum += t->p[last-1];
    last -= lsb(last);
  }
  while(first > last){
    assert(sum - t->p[first-1] <= sum);
    sum -= t->p[first-1];
    first -= lsb(first); 
  }
  return sum;
}

