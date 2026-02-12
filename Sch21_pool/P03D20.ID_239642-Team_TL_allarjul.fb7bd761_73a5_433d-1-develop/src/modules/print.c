#include "print.h"

#include "translate_and_calculate.h"

void print(list* lst) {
    double x_step = 4 * M_PI / (COLS - 1);
    for (int y = -(ROWS - 1) / 2; y <= (ROWS - 1) / 2; y++) {
        for (double x = 0; x < COLS; x++) {
            double arg = x * x_step;
            int rounded_func = (int)round(calculate_expression(lst, arg) * (ROWS - 1) / 2);
            if (rounded_func == y)
                printf("*");
            else
                printf(".");
        }
        printf("\n");
    }
}