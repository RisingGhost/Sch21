#include <math.h>
#include <ncurses.h>
#include <stdio.h>
//-lncurses
double next_ball_x(double ball_x, int angl);
double next_ball_y(double ball_y, int angl);
int rocket_reflection(int angl);
int border_reflection(int angl);
int reflection(double ball_x, double ball_y, int angl, int rock1_y, int rock2_y, int columns, int rows);
void pong_display(double ball_x, double ball_y, int rock1_y, int rock2_y, int columns, int rows, int player1,
                  int player2);
int check_winner(int player1, int player2);
void goal(int width);
void set_terminal_size(int columns, int rows);
int new_rock1_y(int rock1_y, char ch, int rows);
int new_rock2_y(int rock2_y, char ch, int rows);
int keyboard(double ball_x, double ball_y, int rock1_y, int rock2_y, int columns, int rows, int player1,
             int player2, char ch);

int main() {
    int rock1_y = 7, rock2_y = 7, angl = 0, player1 = 0, player2 = 0, columns = 80, rows = 25, ticks = 0,
        target_ticks = 5;
    double ball_x = 4, ball_y = rock1_y;
    initscr(), cbreak(), noecho(), nodelay(stdscr, TRUE), curs_set(0);
    pong_display(ball_x, ball_y, rock1_y, rock2_y, columns, rows, player1, player2);
    while (1) {
        ticks++;

        if ((int)ball_x == 0)
            player2++, ball_y = rock1_y, ball_x = 3, angl = 0;
        else if ((int)ball_x == columns - 1)
            player1++, ball_y = rock2_y, ball_x = columns - 4, angl = 180;
        if (check_winner(player1, player2)) return 0;
        if (ticks >= target_ticks)
            ticks = 0,
            pong_display(ball_x = next_ball_x(ball_x, angl), ball_y = next_ball_y(ball_y, angl), rock1_y,
                         rock2_y, columns, rows, player1, player2),
            angl = reflection(ball_x, ball_y, angl, rock1_y, rock2_y, columns, rows);
        char ch;
        ch = getch();
        int key = keyboard(ball_x, ball_y, rock1_y = new_rock1_y(rock1_y, ch, rows),
                           rock2_y = new_rock2_y(rock2_y, ch, rows), columns, rows, player1, player2, ch);
        if (!key) {
            endwin();
            return 0;
        } else if (key == 2) {
            napms(6);
            set_terminal_size(columns, rows);
        }
    }
    endwin();
    return 0;
}

void pong_display(double ball_x, double ball_y, int rock1_y, int rock2_y, int columns, int rows, int player1,
                  int player2) {
    clear();
    ball_x = (int)ball_x;
    ball_y = (int)ball_y;
    set_terminal_size(columns, rows);

    for (int i = 0; i < rows; i++) {
        // отрисовка полей
        if (i == 0 || i == rows - 1) {
            for (int j = 0; j <= columns; j++) {
                if (j == columns)
                    addch('\n');
                else
                    addch('-');
            }
        }
        // здесь внутри уже добавляем работу с мячиком и рокетками
        else {
            for (int j = 0; j <= columns; j++) {
                if ((i == ball_y) && (j == ball_x))
                    addch('*');
                else if ((j == columns / 4) && (i == rows / 9) && (player1 < 10))
                    addch('0' + player1);
                else if ((j == 3 * columns / 4) && (i == rows / 9) && (player2 < 10))
                    addch('0' + player2);
                else if ((j == columns / 4) && (i == rows / 9) && (player1 > 9)) {
                    addch('0' + (player1 / 10));
                    addch('0' + (player1 % 10));
                } else if ((j == 3 * columns / 4) && (i == rows / 9) && (player2 > 9)) {
                    addch('0' + (player2 / 10));
                    addch('0' + (player2 % 10));
                } else if (((i == rock1_y + 1) || (i == rock1_y - 1) || (i == rock1_y)) && (j == 2))
                    addch('|');
                else if (((i == rock2_y + 1) || (i == rock2_y - 1) || (i == rock2_y)) && (j == columns - 3))
                    addch('|');
                else if (j == columns / 2 || j == 0 || j == columns - 1)
                    addch('|');
                else if (j == columns)
                    addch('\n');
                else if ((i == rows / 9) && (player1 > 9) && (player2 > 9) &&
                         ((j == 2) || (j == columns - 4)))
                    continue;
                else if ((i == rows / 9) && (player1 <= 9) && (player2 > 9) && (j == columns - 4))
                    continue;
                else if ((i == rows / 9) && (player1 > 9) && (player2 <= 9) && (j == 2))
                    continue;
                else
                    addch(' ');
            }
        }
    }
    refresh();
}

double next_ball_x(double ball_x_f, int angl) {
    // printf("%lf", ball_x_f);
    ball_x_f = ball_x_f + 1 * cos(angl * 3.14 / 180);
    // printf("%lf", ball_x_f);
    return ball_x_f;
}
double next_ball_y(double ball_y_f, int angl) {
    ball_y_f = ball_y_f + 1 * sin(angl * 3.14 / 180);
    return ball_y_f;
}
int rocket_reflection(int angl) {
    angl = 180 - angl;
    return angl;
}
int border_reflection(int angl) {
    angl = -angl;
    return angl;
}
int reflection(double ball_x, double ball_y, int angl, int rock1_y, int rock2_y, int columns, int rows) {
    ball_x = (int)ball_x;
    ball_y = (int)ball_y;
    if ((ball_y == 1) || (ball_y == rows - 2)) {
        angl = border_reflection(angl);
    } else if (ball_x == 3 && ball_y == rock1_y) {  // центр первой ракетки
        angl = 0;
    } else if (ball_x == columns - 4 && ball_y == rock2_y) {  // центр второй ракетки
        angl = 180;
    } else if (angl == 180 && ball_x == 3 && ball_y == rock1_y - 1) {  // угол 180 первая ракетка верх
        angl = -25;
    } else if (angl == 180 && ball_x == 3 && ball_y == rock1_y + 1) {  // угол 180 первая ракетка низ
        angl = 25;
    } else if (angl == 0 && ball_x == columns - 4 &&
               ball_y == rock2_y - 1) {  // угол ноль вторая ракетка верх
        angl = -155;
    } else if (angl == 0 && ball_x == columns - 4 && ball_y == rock2_y + 1) {  // угол ноль вторая ракетка низ
        angl = 155;
    } else if (ball_x == 3 && (ball_y == rock1_y + 1 || ball_y == rock1_y - 1)) {  // края первая ракетка
        angl = rocket_reflection(angl);
    } else if (ball_x == columns - 4 &&
               (ball_y == rock2_y + 1 || ball_y == rock2_y - 1)) {  // края вторая ракетка
        angl = rocket_reflection(angl);
    }
    return angl;
}

void set_terminal_size(int columns, int rows) { printf("\033[8;%d;%dt", rows + 3, columns+3); }

int check_winner(int player1, int player2) {
    if (player1 == 21) {
        printf("\n\n\n\n\n");
        printf("        PLAYER 1 - WINNER        ");
        printf("                ");
        return 1;
    } else if (player2 == 21) {
        printf("\n\n\n\n\n");
        printf("        PLAYER 2 - WINNER        ");
        printf("                ");
        return 1;
    } else
        return 0;
}

int keyboard(double ball_x, double ball_y, int rock1_y, int rock2_y, int columns, int rows, int player1,
             int player2, char ch) {
    ball_x = (int)ball_x;
    ball_y = (int)ball_y;
    if (ch == 'q')
        return 0;
    else if ((ch == 'a') || (ch == 'z') || (ch == 'm') || (ch == 'k')) {
        pong_display(ball_x, ball_y, rock1_y, rock2_y, columns, rows, player1, player2);
        return 1;
    } else
        return 2;
}

int new_rock1_y(int rock1_y, char ch, int rows) {
    if (ch == 'a' && rock1_y > 2) {
        rock1_y = rock1_y - 1;
    } else if (ch == 'z' && rock1_y < rows - 3) {
        rock1_y = rock1_y + 1;
    }
    return rock1_y;
}

int new_rock2_y(int rock2_y, char ch, int rows) {
    if (ch == 'k' && rock2_y > 2) {
        rock2_y = rock2_y - 1;
    } else if (ch == 'm' && rock2_y < rows - 3) {
        rock2_y = rock2_y + 1;
    }
    return rock2_y;
}