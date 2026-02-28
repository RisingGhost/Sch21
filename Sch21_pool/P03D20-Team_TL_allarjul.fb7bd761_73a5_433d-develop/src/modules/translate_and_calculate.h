#ifndef TR_N_CALC
#define TR_N_CALC

#include "../libraries/list.h"
#include "../libraries/stack.h"
#include "../libraries/stack_double.h"

int to_polish_notation(list* lst, list* res_lst);
double calculate_func(double arg, char func);
double calculate_operator(double first, double second, char operator);
double calculate_expression(list* lst, double x);
int is_good_input(list* str);

#endif
