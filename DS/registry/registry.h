#ifndef REGISTRY_NAIVE_H
#define REGISTRY_NAIVE_H

// Data structure based on Sean parent's presentation Better Code: Relationships
// https://sean-parent.stlab.cc/papers-and-presentations/#better-code-relationships
// It associates an ID with some data that is stored and can be latter accessed. 
// It replaces the std::map data structure. 
// It is implemented as an ordered array (key_id is a monotonically increasing 
// value) so that searches are always O(logN) and memory is always contiguous,
// contrary to the std::map that is a node based data structure
// It shrinks, compacts and expands as neccessary

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


typedef struct {
  void* arr;  
  size_t sz;
  size_t cap;
  size_t occ_bucket;
  size_t elm_sz;
  // monotonic increasing key id 
  size_t key_id;
} registry_t;


void init_registry(registry_t* reg, size_t elm_sz);

void free_registry(registry_t* reg);

// Get a reference to the value type. 
void* find_registry(registry_t* reg, uint32_t key);

void delete_registry(registry_t* reg, uint32_t key);

// Value semantic. i.e., the void* value will be copied into the registry. Shallow copy 
uint32_t push_back_registry(registry_t* reg, void* value, size_t elm_sz); 

// Just for test purposes
void test_invariants_registry_hold(registry_t* reg);
 
#endif

