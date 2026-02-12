#include <stdio.h>
#include <math.h>

double next_ball_x (double ball_x, int angl);
double next_ball_y (double ball_y, int angl);
int rocket_reflection(int angl);
int border_reflection(int angl);
int reflection(double ball_x, double ball_y, int angl, int rock1_y, int rock2_y, const int columns, const int rows);
void pong_display(double ball_x, double ball_y, int rock1_y, int rock2_y, const int columns, const int rows,  int player1, int player2);
void gol() {return;}

int main()
{
    double ball_x, ball_y;
    int rock1_y, rock2_y, angl, player1 = 0, player2 = 0;
    char ch;
    const int columns = 80, rows = 25;

    rock1_y = 7;
    rock2_y = 7;
    ball_x = 3;
    ball_y = rock1_y;
    angl = -45;
    
    pong_display(ball_x,ball_y,rock1_y,rock2_y,columns,rows, player1, player2);


    while (1)
    {
        
        if ((int)ball_x == 0) {
                player1++;
                ball_y = rock1_y;
                ball_x = 3;
                angl = 0;
                gol();
                ch = getchar();
            }

        else if ((int)ball_x == columns-1) {
 
                player2++;
                ball_y = rock2_y;
                ball_x = columns-4;
                angl = 180;
                gol();
                ch = getchar();
            }

        if (player1 == 21)
        {
            printf("\n\n\n\n\n");
            printf("        PLAYER 1 - WINNER        ");
        }
        else if (player2 == 21)
        {
            printf("\n\n\n\n\n");
            printf("        PLAYER 2 - WINNER        ");
            printf("                ");
        }

        

        scanf("%c", &ch);
        
        if (ch == 'a') {
            if (rock1_y>2) pong_display(ball_x = next_ball_x(ball_x, angl), ball_y = next_ball_y(ball_y, angl), rock1_y = rock1_y - 1, rock2_y,columns,rows, player1, player2);
        }
        else if (ch == 'z') {
            if (rock1_y<rows-3) pong_display(ball_x = next_ball_x(ball_x, angl), ball_y = next_ball_y(ball_y, angl), rock1_y = rock1_y + 1, rock2_y,columns,rows, player1, player2);

        }
        else if (ch == 'k') {
            if (rock2_y>2) pong_display(ball_x = next_ball_x(ball_x, angl), ball_y = next_ball_y(ball_y, angl), rock1_y, rock2_y = rock2_y - 1,columns,rows, player1, player2);


        }
        else if (ch == 'm') {
            if (rock2_y<rows-3) pong_display(ball_x = next_ball_x(ball_x, angl), ball_y = next_ball_y(ball_y, angl), rock1_y, rock2_y = rock2_y + 1,columns,rows, player1, player2);

        }
        else if (ch == ' ') {
            pong_display(ball_x = next_ball_x(ball_x, angl), ball_y = next_ball_y(ball_y, angl), rock1_y, rock2_y ,columns,rows, player1, player2);

        }
        else continue;
        
        angl = reflection(ball_x,ball_y,angl,rock1_y,rock2_y,columns,rows);
    }

    return 0;
}



void pong_display(double ball_x, double ball_y, int rock1_y, int rock2_y, const int columns, const int rows, int player1, int player2) {

    ball_x = (int)ball_x;
    ball_y = (int)ball_y;

    

    for (int i = 0; i < rows; i++)
    {
        
        //отрисовка полей
        if (i == 0 || i == rows-1) {
            for (int j = 0; j <= columns; j++) 
            { 
                if (j == columns)   printf("\n");
                else printf("-"); 
            }
        }
        //здесь внутри уже добавляем работу с мячиком и рокетками
        else
        { 
        for (int j = 0; j <= columns; j++)
            {
            if ((i == ball_y) && (j == ball_x)) printf("*");
            else if ((j == columns/4) && (i == rows/9)) printf("%d", player1);
            else if ((j == 3*columns/4) && (i == rows/9)) printf("%d", player2);
            else if (((i == rock1_y+1) || (i == rock1_y-1) || (i == rock1_y)) && (j == 2)) printf("|");
            else if (((i == rock2_y+1) || (i == rock2_y-1) || (i == rock2_y)) && (j == columns - 3)) printf("|");
            else if (j == columns/2 || j == 0 || j == columns-1) printf("|");
            else if (j == columns)   printf("\n");
            else printf(" ");
            }
        }
    }
}




double next_ball_x (double ball_x_f, int angl) {
    //printf("%lf", ball_x_f);
    ball_x_f = ball_x_f + 1 * cos(angl*3.14/180);
    //printf("%lf", ball_x_f);
    return ball_x_f;
}

double next_ball_y (double ball_y_f, int angl) {
    ball_y_f = ball_y_f + 1 * sin(angl* 3.14/180);
    return ball_y_f;
} 
int rocket_reflection(int angl){
    angl = 180-angl;
    return angl;
}
int border_reflection(int angl){
    angl = -angl;
    printf("%d", angl);
    return angl;
}


int reflection(double ball_x, double ball_y, int angl, int rock1_y, int rock2_y, const int columns, const int rows)
{
    ball_x = (int)ball_x;
    ball_y = (int)ball_y;
    if ((ball_y == 2)||(ball_y == rows-2)){
        angl = border_reflection(angl);
        printf("\n\n\n\n\n");
        }
    else if (ball_x == 2 && ball_y == rock1_y){ // центр первой ракетки
        angl = 0;
        }
    else if (ball_x == columns-3 && ball_y == rock2_y){ // центр второй ракетки
        angl = 180;
        }
    else if (angl == 180 && ball_x == 3 && ball_y == rock1_y-1){ // угол 180 первая ракетка верх
        angl = -30;
        printf("ANGL = 180, LEFT_TOP\n");
        }
    else if (angl == 180 && ball_x == 2 && ball_y == rock1_y+1){ // угол 180 первая ракетка низ
        angl = 30;
        printf("ANGL = 180, LEFT_BOT\n");
        }
    else if (angl == 0 && ball_x == columns-3 && ball_y == rock2_y-1){ // угол ноль вторая ракетка верх
        angl = -150;
        printf("ANGL = 0, RIGHT_TOP\n");
        }
    else if (angl == 0 && ball_x == columns-3 && ball_y == rock2_y+1){ //угол ноль вторая ракетка низ
        angl = 150;
        printf("ANGL = 0, RIGHT_BOT\n");
        }
    else if (ball_x == 2 && (ball_y == rock1_y+1||ball_y == rock1_y-1)){ // края первая ракетка
        angl = rocket_reflection(angl);
        printf("LAST CHECK LEFT Top_n_Bot\n");
        }
    else if (ball_x == columns-3 && (ball_y == rock2_y+1||ball_y == rock2_y-1)){ // края вторая ракетка
        angl = rocket_reflection(angl);
        printf("LAST CHECK RIGHT Top_n_Bot\n");
        }
    return angl;
}
