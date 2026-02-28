#include "stack.h"

stack* init() {
    int is_nice = 1;
    stack* st = (stack*)malloc(sizeof(stack));
    if (!st) is_nice = 0;
    if (is_nice) {
        st->cap = 10;
        st->size = 0;
        st->data = (char*)malloc(sizeof(char) * st->cap);
        if (!st->data) {
            is_nice = 0;
            free(st);
        }
    }

    return is_nice ? st : NULL;
}

int push(stack* st, char value) {
    int is_nice = 1;
    if (st->cap == st->size) {
        st->cap *= 2;
        char* tmp = (char*)realloc(st->data, st->cap);
        if (!tmp) is_nice = 0;
        if (is_nice) st->data = tmp;
    }

    if (is_nice) {
        st->data[(st->size)++] = value;
    }

    return is_nice ? 1 : 0;
}

int pop(stack* st, char* value) {
    int is_nice = 1;
    if (st->size == 0) is_nice = 0;
    if (is_nice) *value = st->data[--(st->size)];
    return is_nice;
}

void destroy(stack* st) {
    free(st->data);
    st->size = 0;
    st->cap = 0;
    free(st);
}
