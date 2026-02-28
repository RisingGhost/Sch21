#include "sort.h"

void sort(double *a, int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (a[j] > a[j + 1]) swap(a + j, a + j + 1);
        }
    }
}

void swap(double *x, double *y) {
    double temp_x = *x, temp_y = *y;
    *x = temp_y;
    *y = temp_x;
}
