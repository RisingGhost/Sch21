#include <stdio.h>
int chet (int x);
int main() {
    int x;
    scanf("%d", &x);
    printf("%d",chet(x));

}

int chet(int x){
    if (x%2 == 0 ) return 0;
    return 1;
}