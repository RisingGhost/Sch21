#ifndef STACK_DBL
#define STACK_DBL

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct stack_double {
    double* data;
    int size;
    int cap;
} stack_double;

stack_double* init_double();
double push_double(stack_double* st, double value);
double pop_double(stack_double* st, double* value);
void destroy_double(stack_double* st);

#endif