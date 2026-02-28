#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#include "libraries/list.h"
#include "modules/parser.h"
#include "modules/print.h"
#include "modules/translate_and_calculate.h"

int main() {
    char* str;
    int error = 0;
    if (!input(&str)) {
        error = 1;
    }
    list* lst = list_init();
    list* res_list = list_init();

    if (!error && !transform_str_to_list(str, lst)) error = 1;
    if (!error && !to_polish_notation(lst, res_list)) error = 1;

    if (!error) {
        print(res_list);
    } else {
        printf("n/a\n");
    }

    list_destroy(lst);
    list_destroy(res_list);
    free(str);
}
