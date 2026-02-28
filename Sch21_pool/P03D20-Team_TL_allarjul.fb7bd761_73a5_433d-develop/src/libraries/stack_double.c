#include "stack_double.h"

stack_double* init_double() {
    int is_nice = 1;
    stack_double* st = (stack_double*)malloc(sizeof(stack_double));
    if (!st) is_nice = 0;
    if (is_nice) {
        st->cap = 10;
        st->size = 0;
        st->data = (double*)malloc(sizeof(double) * st->cap);
        if (!st->data) {
            is_nice = 0;
            free(st);
        }
    }

    return is_nice ? st : NULL;
}

double push_double(stack_double* st, double value) {
    int is_nice = 1;
    if (st->cap == st->size) {
        st->cap *= 2;
        double* tmp = (double*)realloc(st->data, st->cap);
        if (!tmp) is_nice = 0;
        if (is_nice) st->data = tmp;
    }

    if (is_nice) {
        st->data[(st->size)++] = value;
    }

    return is_nice ? 1 : 0;
}

double pop_double(stack_double* st, double* value) {
    int is_nice = 1;
    if (st->size == 0) is_nice = 0;
    if (is_nice) *value = st->data[--(st->size)];
    return is_nice;
}

void destroy_double(stack_double* st) {
    free(st->data);
    st->size = 0;
    st->cap = 0;
    free(st);
}
