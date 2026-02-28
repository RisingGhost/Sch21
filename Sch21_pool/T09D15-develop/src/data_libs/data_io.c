#include "data_io.h"

void input(double **data, int *n) {
    if (scanf("%d", n) != 1|| *n <= 0 ) *n = -1;
    *data = (double *)malloc( *n * sizeof(double));
    for (double *p = *data; p - *data < *n; p++) {
        if ((p - *data < *n)&&(scanf("%lf", p)) !=1 ) *n = -1;
    }   
}

void output(double *data, int n) {
    for (int i = 0; i < n; i++) {
        if (i < n-1 ) printf("%.2lf ", data[i]);
        else printf("%.2lf", data[i]);
    }
    
}