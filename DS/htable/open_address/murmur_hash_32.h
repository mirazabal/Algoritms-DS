#ifndef MURMUR_HASH_WIKI_32
#define MURMUR_HASH_WIKI_32 

// Murmur Hash implementation from Wikipedia
// https://en.wikipedia.org/wiki/MurmurHash

#include <stddef.h>
#include <stdint.h>

uint32_t murmur3_32(const uint8_t* key, size_t len, uint32_t seed);


#endif

