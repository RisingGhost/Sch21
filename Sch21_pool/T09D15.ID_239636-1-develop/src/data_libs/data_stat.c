#include "data_stat.h"

double max(double *a, int n) {
    double max = a[0];
    for (double *p = a; p - a < n; p++) {
        if (max < *p) max = *p;
    }
    return max;
}
double min(double *a, int n) {
    double min = a[0];
    for (double *p = a; p - a < n; p++) {
        if (min > *p) min = *p;
    }
    return min;
}
double mean(double *a, int n) {
    double sum = 0;
    for (double *p = a; p - a < n; p++) {
        sum += *p;
    }
    double mean = sum / (double)n;
    return mean;
}
double variance(double *a, int n) {
    double variance = 0, v_diff = 0;
    for (double *p = a; p - a < n; p++) {
        v_diff = *p - mean(a, n);
        variance += v_diff * v_diff;
    }
    variance /= n;
    return variance;
}
 