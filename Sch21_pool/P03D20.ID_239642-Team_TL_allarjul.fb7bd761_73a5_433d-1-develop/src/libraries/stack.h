#ifndef STACK
#define STACK

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct stack {
    char* data;
    int size;
    int cap;
} stack;

stack* init();
int push(stack* st, char value);
int pop(stack* st, char* value);
void destroy(stack* st);

#endif