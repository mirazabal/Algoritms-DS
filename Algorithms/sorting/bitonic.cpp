/*
 * Naive bitonic sort, from
 * K. E. Batcher. 1968. Sorting networks and their applications. In Proceedings of the April 30--May 2, 1968, spring joint computer conference (AFIPS '68 (Spring)). Association for Computing Machinery, New York, NY, USA, 307–314. DOI:https://doi.org/10.1145/1468075.1468121
 *
 */

#include <algorithm>
#include <cassert>
#include <chrono>
#include <iterator>
#include <iostream>
#include <functional>
#include <random>
#include <vector>

template<typename T, typename C> 
void _sort_bitonic(T first, T last, C comp)
//  requires random_access_iterator<T>
{
  auto d = std::distance(first,last);
  auto it = first;
  std::advance(it, d/2);
  while(it != last){
    if(comp(*it, *first))
        std::iter_swap(first,it);
    std::advance(it, 1);
    std::advance(first, 1);
  }
}

template<typename T, typename C> 
void sort_bitonic_seq(T first, T last, C comp)
//  requires random_access_iterator<T>
{
  // assert([first,last) is a bitonic sequence
  auto n = std::distance(first,last);
  assert(n > -1);
  auto d = n;
  while(d > 1){
    auto it_f = first;
    auto it_l = first; 
    std::advance(it_l, d);
    for(int i = 0; i < n/d; ++i){
      _sort_bitonic(it_f, it_l, comp);
      std::advance(it_f, d);
      std::advance(it_l, d);
    }    
    d = d/2;
  }
}
  
template<typename T>
void gen_bitonic_seq(T first, T last)
//  requires random_access_iterator<T>
{
  using ValueType = typename std::iterator_traits<T>::value_type;
  uint32_t s = 2;
  auto d = std::distance(first, last);
  assert(d > -1);
  
  while(s < d){
    const uint32_t chunks = d/s; 
    auto it_f = first;
    auto it_l = first;
    std::advance(it_l,s);
    for(int i = 0; i < chunks/2; ++i){
      sort_bitonic_seq(it_f, it_l, std::less<ValueType>());
      std::advance(it_f, s*2);
      std::advance(it_l, s*2);
    } 
    it_f = first;
    std::advance(it_f,s);
    it_l = it_f;
    std::advance(it_l,s);
    for(int i = 0; i < chunks/2; ++i){
      sort_bitonic_seq(it_f, it_l, std::greater<ValueType>());
      std::advance(it_f, s*2);
      std::advance(it_l, s*2);
    } 
    s = s << 1;
  }
}

template<typename T> 
void bitonic_sort(T first, T last)
//  requires random_access_iterator<T>
{
  using ValueType = typename std::iterator_traits<T>::value_type;
  gen_bitonic_seq(first,last);
  sort_bitonic_seq(first,last,std::less<ValueType>());
}


int main()
{
  std::vector<int> v(65536); 
  std::iota(std::begin(v), std::end(v), 0);
  std::shuffle(v.begin(), v.end(), std::mt19937{std::random_device{}()});

  auto start = std::chrono::steady_clock::now();
  bitonic_sort(std::begin(v), std::end(v));
  auto end = std::chrono::steady_clock::now();
  auto elapsed_bitonic = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count();
  assert(std::is_sorted(std::begin(v),std::end(v)));

  std::vector<int> v_2(65536); 
  std::iota(std::begin(v_2), std::end(v_2), 0);
  std::shuffle(v_2.begin(), v_2.end(), std::mt19937{std::random_device{}()});

  start = std::chrono::steady_clock::now();
  std::sort(std::begin(v_2), std::end(v_2));
  end = std::chrono::steady_clock::now();
  auto elapsed_intro = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count();

  std::cout << "std::sort took = " << elapsed_intro << " and bitonic sort = " << elapsed_bitonic;

  return 0;
}

