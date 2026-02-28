#include "types.h"

int is_function(char* str, int* len) {
    int res = 0;
    char* funcs[] = {"sin", "cos", "tan", "ctg", "sqrt", "ln"};
    for (int i = 0; i < 6 && res == 0; ++i) {
        if (strncmp(str, funcs[i], strlen(funcs[i])) == 0) {
            *len = strlen(funcs[i]);
            res = 1;
        }
    }

    return res;
}

int is_digit(char c) { return (c >= '0' && c <= '9'); }

int is_space(char c) { return (c == ' ' || c == '\t'); }

int is_special_function(char c) {
    return (c == 's' || c == 'c' || c == 't' || c == 'g' || c == 'q' || c == 'l');
}

int is_operator(char c) { return (c == '*' || c == '/' || c == '-' || c == '+' || c == '~'); }
