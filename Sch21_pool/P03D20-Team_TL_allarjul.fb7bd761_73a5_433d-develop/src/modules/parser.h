#ifndef PARSER
#define PARSER

#include <stdlib.h>

#include "../libraries/list.h"
#include "types.h"

int input(char** str);
int transform_str_to_list(char* str, list* lst);
int add_digit_lexem(list* lst, char** ptr);

#endif