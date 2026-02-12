#include <stdio.h>
#include <ncurses.h>
#include <stdlib.h>

#define cols 80
#define rows 25

int main_game(int *field[rows][cols], int *time, int *mstk);
int read_initial_state(int field[rows][cols]);
void print_field(int field[rows][cols]);
void draw_field(int matr[rows][cols]);
void input(int matr[rows][cols]);
void update_field(int field[rows][cols]);
int alive_or_not(int q[rows][cols], int i, int j);

int main(void) {
    int field[rows][cols];

    if (!read_initial_state(field)) printf("n/a");
    else
    {
        // print_field(field);
        freopen("/dev/tty", "r", stdin);
        initscr();
        noecho();
        nodelay(stdscr, TRUE);
        curs_set(0);
        int time = 500, mstk = 0;
        main_game(field, &time, &mstk);
        endwin();
    }
    return 0;
}


int main_game(int *field[rows][cols], int *time, int *mstk){
    char ch;
    while (mstk != 1){
        draw_field(field);
        update_field(field);
        napms(time);
        if ((ch = getch()) == ' ') mstk = 1;
        else if ((ch = getch()) == 'a') time -= 100; 
        else if ((ch = getch()) == 'z') time += 100; 
    }
}
int read_initial_state(int field[rows][cols]) {
    char line[cols + 2];  // +2 to account for newline and null terminator
    for (int i = 0; i < rows; i++) {
        if (!fgets(line, sizeof(line), stdin)) {
            return 0;
        }
        for (int j = 0; j < cols; j++) {
            if (line[j] == '1') {
                field[i][j] = 1;
            } else if (line[j] == '0') {
                field[i][j] = 0;
            } else {
                return 0;
            }
        }
    }

    return 1;
}

void draw_field(int matr[rows][cols]) { 
    clear();
    for (int y = 0; y < rows; y++) {
        for (int x = 0; x < cols; x++) {
            mvaddch(y, x, matr[y][x] ? 'x' : '-');
        }
    }
    refresh();
}

void update_field(int matr[rows][cols]) {

int **new_matr = malloc(rows * sizeof(int *));
for (int i = 0; i < rows; i++) {
    new_matr[i] = malloc(cols * sizeof(int));
}

    for (int x = 0; x < rows; x++) 
        for (int y = 0; y < cols; y++) new_matr[x][y] = alive_or_not(matr, x , y);

    for (int x = 0; x < rows; x++)
        for (int y = 0; y < cols; y++) matr[x][y] = new_matr[x][y];

for (int i = 0; i < rows; i++) {
    free(new_matr[i]);
}
free(new_matr);

}

int alive_or_not(int q[rows][cols], int x, int y) {

    int count_alive = 0, r = q[x][y];   // r - возврат состояня будущей клетки

    for (int i = -1; i < 2; i++)
        for (int j = -1; j < 2; j++)
        {
            if (i == 0 && j == 0) continue;
            else if (q[(rows+x +i)%rows][(cols + y + j)%cols] == 1) count_alive++;
        }

            
    if (q[x][y] == 0 && count_alive == 3) r = 1;
    else if (q[x][y] == 1 && count_alive > 3) r = 0;
    else if (q[x][y] == 1 && count_alive < 2) r = 0;
    return r;
}



void print_field(int field[rows][cols]) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            printf("%c", field[i][j] ? '1' : '0');
        }
        printf("\n");
    }
}
