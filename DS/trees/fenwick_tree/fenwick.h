/*
 * Naive implementation from Fenwick's paper: 
 * @article{https://doi.org/10.1002/spe.4380240306,
author = {Fenwick, Peter M.},
title = {A new data structure for cumulative frequency tables},
journal = {Software: Practice and Experience},
volume = {24},
number = {3},
pages = {327-336},
keywords = {Binary indexed tree, Arithmetic coding, Cumulative frequencies},
doi = {https://doi.org/10.1002/spe.4380240306},
url = {https://onlinelibrary.wiley.com/doi/abs/10.1002/spe.4380240306},
eprint = {https://onlinelibrary.wiley.com/doi/pdf/10.1002/spe.4380240306},
year = {1994}
}
*/

#include <stdint.h>

typedef struct fenwick_s
{
  uint32_t* p;
  uint32_t size;
} fwck_t ;

fwck_t fwck_init(uint32_t size);

void fwck_free(fwck_t* t);

void fwck_add(fwck_t* t, uint32_t pos, uint32_t delta);

void fwck_del(fwck_t* t, uint32_t pos, uint32_t delta);

// Close-open interval [ , )
uint32_t fwck_acc(fwck_t* t, uint32_t first, uint32_t last);
