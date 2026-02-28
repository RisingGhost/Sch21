#include <stdio.h>
#define row 3
#define col 3

int alive_or_not(int q[row][col], int i, int j);

int main() {

int q[row][col];
int i = 1, j = 1;
}

// e[i][j] = alive_or_not(q[i][j]);

int alive_or_not(int q[row][col], int x, int y) {

    int count_alive = 0, r = q[x][y];   // r - возврат состояня будущей клетки

    for (int i = -1; i < 2; i++)
        for (int j = -1; j < 2; j++)
        {
            if (i == 0 && j == 0) continue;
            else if (q[(row+x +i)%row][(col + y + j)%col] == 1) count_alive++;
        }

            
    if (q[x][y] == 0 && count_alive == 3) r = 1;
    else if (q[x][y] == 1 && count_alive > 3) r = 0;
    else if (q[x][y] == 1 && count_alive < 2) r = 0;
    return r;
}