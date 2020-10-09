/*
 * Experimental partial retroactive queue
 * https://erikdemaine.org/papers/Retroactive_TALG/paper.pdf
 */


#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t s_time = 0;

typedef struct pr_node_s{
  struct pr_node_s* next;
  struct pr_node_s* prev;
  int64_t time;
  int64_t val;
} pr_node_t;

typedef struct pr_queue {
  pr_node_t* f;
  pr_node_t* b;
} pr_queue_t;

pr_queue_t pr_queue_init()
{
 pr_queue_t q; // = malloc(sizeof(pr_queue_t));
 q.f = NULL;
 q.b = NULL;
 return q;
}

void enqueue(pr_queue_t* q, int64_t val)
{
   pr_node_t* node = malloc(sizeof(pr_node_t));
   node->next = NULL;
   node->prev = q->b;
   if(q->b != NULL)
      q->b->next = node;
   node->val = val;
   s_time += 100; 
   node->time = s_time; 
   q->b = node;
   if(q->f == NULL) 
     q->f = node;
}

void retro_insert_enqueue(pr_queue_t* q, int64_t time, int64_t val)
{
  pr_node_t* new_node = malloc(sizeof(pr_node_t));
  new_node->time = time;
  new_node->val = val;
  pr_node_t* n = q->f;
  if(n == NULL){
    q->f = new_node; 
    return;
  }

  if(n->time > time){ // move backwards
    while(n->prev != NULL && n->prev->time > time){
      n = n->prev;
    }
    if(n->prev != NULL){
      n->prev->next = new_node;
      new_node->next = n;
      new_node->prev = n->prev;
      n->prev = new_node;
    } else {
      new_node->next = n;
      n->prev = new_node;
    }
    q->f = q->f->prev; 
  } else { // move forwards
    while(n->next != NULL && time > n->next->time){
      n = n->next;
    } 
    if(n->next != NULL){
      new_node->next = n->next;
      n->next = new_node;
      new_node->next->prev = new_node;
      new_node->prev = n;
    } else {
      n->next = new_node;
      new_node->prev = n;
    }
  }
}

void retro_delete_enqueue(pr_queue_t* q, int64_t time)
{
  pr_node_t* n = q->f;
  assert(n != NULL && "Cannot delete an enqueue if the enqueue did not exist");
  if(n->time < time){ // move forwards
    while(n != NULL && n->time != time ){
      n = n->next;  
    } 
    assert(n != NULL && "Time value not found!!!");
    if(n->next != NULL)
      n->next->prev = n->prev; 
    if(n->prev != NULL)
      n->prev->next = n->next;
  } else { // move backwards 
     while(n != NULL && n->time != time ){
      n = n->prev;  
    }  
    assert(n != NULL && "Time value not found!!!");
    if(n->next != NULL)
      n->next->prev = n->prev; 
    if(n->prev != NULL)
      n->prev = n->next;
    q->f = q->f->next;
  } 
  free(n);
  n = NULL;
}

void dequeue(pr_queue_t* q)
{
  assert(q != NULL);
  if(q->f != NULL)
    q->f = q->f->next;
}

void retro_insert_dequeue(pr_queue_t* q, int64_t time)
{
  assert(q != NULL);
  if(q->f != NULL)
    q->f = q->f->next;
}

void retro_delete_dequeue(pr_queue_t* q, int64_t time)
{
  assert(q != NULL);
  if(q->f != NULL)
    q->f = q->f->prev;
}

int64_t front(pr_queue_t* q)
{
  if(q->f != NULL)
    return q->f->val; 
  return 0;
}

int64_t back(pr_queue_t* q)
{
  if(q->b != NULL)
    return q->b->val;
  return 0;
}

int main()
{
  pr_queue_t q = pr_queue_init();
  
  enqueue(&q, 10); // time 100
  enqueue(&q, 20); // time 200
  enqueue(&q, 30); // time 300
  retro_insert_enqueue(&q,150,15); // time 150
  retro_insert_enqueue(&q,175,17); // time 150

  printf("Front = %ld \n", front(&q));
  dequeue(&q);
  retro_delete_enqueue(&q, 175);
  printf("Front = %ld \n", front(&q));

  dequeue(&q);
  printf("Front = %ld \n", front(&q));

  dequeue(&q);
  dequeue(&q);
  enqueue(&q, 40); // time 400
  printf("Front = %ld \n", front(&q));

}

