/*
    Search module for the desired value from data array.

    Returned value must be:
        - "even"
        - ">= mean"
        - "<= mean + 3 * sqrt(variance)"
        - "!= 0"

        OR

        0
*/

#include <stdio.h>
#define NMAX 30

int input(int *a, int *n);
void output(int *a, int n);
int max(int *a, int n);
int min(int *a, int n);
double mean(int *a, int n);
double variance(int *a, int n);
int search(int *a, int n);
int chet(int x);
int triple_sigma(int x, int *a, int n);

void output_result(int max_v, int min_v, double mean_v, double variance_v);

int main()
{
    int n, data[NMAX];
    if (input(data, &n) != 0) return 0;
    output(data, n);    
    output_result(max(data, n), min(data, n), mean(data, n), variance(data, n));

    return 0;
}
int search(int *a, int n){
    for (int *p = a; p - a < n; p++) {
        if (chet(*p) == 1 && *p >= mean(a, n) && *p != 0 && triple_sigma(*p, a, n) == 1){

        }
    }
}
int triple_sigma(int x, int *a, int n){
    int t_diff = 3*variance(a,n);
    if (x < mean(a,n) + t_diff && x > mean(a,n) - t_diff) return 0;
    return 1;
}
int chet(int x){
    if (x%2 == 0 ) return 0;
    return 1;
}
int input(int *a, int *n) {
    char checker;
    if (scanf("%d%c", n, &checker) != 2 || checker != '\n'|| *n <= 0 ) {
        printf("n/a");
        return 1;
    } else {
        for (int *p = a; p - a < *n; p++) {
            if (p - a < *n - 1) {
                if (scanf("%d%c", p, &checker) != 2 || checker != ' ') {
                    printf("n/a");
                    return 1;
                }
            } else if (scanf("%d%c", p, &checker) != 2 || checker != '\n') {
                printf("n/a");
                return 1;
            }
        }
    }
    return 0;
}
void output(int *a, int n) {
    for (int *p = a; p - a < n; p++) {
        if ( p - a < n-1) printf("%d ", *p);
        else printf("%d\n", *p);
    }
}
int max(int *a, int n){
    int max = 0;
    for (int *p = a; p - a < n; p++) {
        if (max < *p) max = *p;
    }
    return max;
}
int min(int *a, int n){
    int min;
    for (int *p = a; p - a < n; p++) {
        if (min > *p) min = *p;
    }
    return min;
}
double mean(int *a, int n){
    int sum = 0;
    for (int *p = a; p - a < n; p++) {
        sum += *p;
    }
    double mean = (double)sum/n; 
    return mean;
}
double variance(int *a, int n){ 
    double variance, v_diff;
    for (int *p = a; p - a < n; p++) {
        v_diff = *p - mean(a, n);
        variance += v_diff * v_diff;
    }
    variance /= n;
    return variance;
}
void output_result(int max_v, int min_v, double mean_v, double variance_v){
    printf("%d %d %.6lf %.6lf", max_v, min_v, mean_v, variance_v);
}

