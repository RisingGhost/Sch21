#include "parser.h"

int input(char** str) {
    int mtk = 0, len = 10;
    *str = (char*)malloc(len * sizeof(char));
    if (*str == NULL) mtk = 1;

    int i = 0;
    char ch = getchar();
    while (mtk == 0 && ch != '\n') {
        if (i < len) {
            (*str)[i] = ch;
            ch = getchar();
            i++;
        } else {
            len *= 2;
            char* tmp = realloc(*str, len);
            if (!tmp) {
                free(*str);
                mtk = 1;
            }
            if (!mtk) *str = tmp;
        }
    }

    return mtk != 1;
}

int add_function_lexem(list* lst, char* ptr, int len) {
    char* buf = (char*)malloc(len + 1);
    if (!buf) return 1;
    if (*ptr == 's' && *(ptr + 1) == 'q') *ptr = 'q';
    if (*ptr == 'c' && *(ptr + 1) == 't') *ptr = 'g';
    strncpy(buf, ptr, len);
    buf[len] = '\0';
    list_add(lst, buf);
    free(buf);
    return 0;
}

int transform_str_to_list(char* str, list* lst) {
    char* ptr = str;
    int error = 0, is_space_str = 1;
    while (error == 0 && *ptr) {
        int len = 0;
        if (is_space(*ptr)) {
            ++ptr;
        } else if (is_function(ptr, &len)) {
            error = add_function_lexem(lst, ptr, len);
            ptr += len;
            is_space_str = 0;
        } else if (*ptr == 'x') {
            char buf[2] = {'x', '\0'};
            list_add(lst, buf);
            ++ptr;
            is_space_str = 0;
        } else if (is_digit(*ptr) || (*ptr == '.' && is_digit(*(ptr + 1)))) {
            if (!add_digit_lexem(lst, &ptr)) error = 1;
            is_space_str = 0;
        } else if (*ptr == '-') {
            if (ptr == str || *(ptr - 1) == '(') {
                list_add(lst, "~");
            } else {
                char buf[2] = {'-', '\0'};
                list_add(lst, buf);
            }
            ++ptr;
            is_space_str = 0;
        } else if (is_operator(*ptr) || *ptr == '(' || *ptr == ')') {
            char buf[2] = {*ptr, '\0'};
            list_add(lst, buf);
            ++ptr;
            is_space_str = 0;
        } else {
            ++ptr;
            error = 1;
            is_space_str = 0;
        }
    }
    if (is_space_str) error = 1;
    return error != 1;
}

int add_digit_lexem(list* lst, char** ptr) {
    int cap = 128, len = 0, error = 0;
    char* buf = (char*)malloc(sizeof(char) * cap);
    int dot_found = 0;
    if (!buf) error = 1;

    while (error == 0 && (is_digit(**ptr) || **ptr == '.')) {
        if (**ptr == '.') {
            if (dot_found) error = 1;
            dot_found = 1;
        }

        if (len + 1 >= cap) {
            cap *= 2;
            char* tmp = realloc(buf, cap);
            if (!tmp) {
                free(buf);
                error = 1;
            }

            if (!error) buf = tmp;
        }

        if (!error) {
            buf[len++] = **ptr;
            (*ptr)++;
        }
    }

    buf[len] = '\0';
    list_add(lst, buf);
    free(buf);
    return error != 1;
}
