#include <stdio.h>
#define NMAX 10

int input(int *a, int *n);
void output(int *a, int n);
void squaring(int *a, int n);

int main() {
    int n, data[NMAX];
    if (input(data, &n) != 0) return 0;
    squaring(data, n);
    output(data, n);
    return 0;
}

int input(int *a, int *n) {
    char checker;
    if (scanf("%d%c", n, &checker) != 2 || checker != '\n' || *n <= 0) {
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

void squaring(int *a, int n) {
    for (int *p = a; p - a < n; p++) {
        *p = *p * *p;
    }
}

void output(int *a, int n) {
    for (int *p = a; p - a < n; p++) {
        if (p - a < n - 1)
            printf("%d ", *p);
        else
            printf("%d", *p);
    }
}
