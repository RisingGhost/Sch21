#ifndef TYPES
#define TYPES

#include <string.h>

int is_function(char* str, int* len);
int is_digit(char c);
int is_space(char c);
int is_operator(char c);
int is_special_function(char c);

#endif