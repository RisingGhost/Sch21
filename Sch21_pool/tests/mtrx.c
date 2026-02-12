#include <stdio.h>

int input_n(int *n);
int input_mtrx(int n, int *data_a, int *data_b);
void count(int n, int *data_a, int *data_b, int *data_c);
void output(int n, int *data);
int output_result(int n, int *data_c);

int main(){
    int n;
    if (input_n(&n) == 1) printf("n/a");
    else{
        int data_a[n*n], data_b[n*n], data_c[n*n];
        if (input_mtrx(n, data_a, data_b) == 1) printf("n\a");
        else {
            output(n, data_a);
            output(n, data_b);
            count(n, data_a, data_b, data_c);
            output(n, data_c);
        }
    }
    return 0;
}

int input_n(int *n){
    int k = 0;
    char chark;
    if (scanf("%d%c", n, &chark)!=2 || chark != ' ' || *n <= 0)
        if (chark != '\n') k = 1;
    return k;
}


int input_mtrx(int n, int *data_a, int *data_b){
    int x, k = 0;
    char chark;
    for (int i = 0; i < 2 * n * n; i++){
        if (scanf("%d%c", &x, &chark)!=2) k = 1;
        if ( i < n * n ) data_a[i] = x;
        else data_b[i-(n * n)] = x;
    }
    return k;
}

void output(int n, int *data){
    for (int i = 0; i < n * n; i++) printf("%d ", data[i]);
    printf("\n");
}

void count(int n, int *data_a, int *data_b, int *data_c){
    for (int i = 0; i < n * n; i++){
        data_c[i]=0;
        int row = i/n;
        int col = i%n;
        for (int j = 0; j < n; j++) data_c[i] += data_a[row*n + j] * data_b[j*n + col];
    }
}

int output_result(int n, int *data_c)
{

}