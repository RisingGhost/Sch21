#include <stdio.h>

#define WIDTH 80
#define HEIGHT 25

int read_initial_state(int field[HEIGHT][WIDTH]);
void print_field(int field[HEIGHT][WIDTH]);

int main(void) {
    int field[HEIGHT][WIDTH];
    if (!read_initial_state(field)) {
        printf("n/a");
        return 1;
    }

    print_field(field);
    return 0;
}

void print_field(int field[HEIGHT][WIDTH]) {
    for (int i = 0; i < HEIGHT; i++) {
        for (int j = 0; j < WIDTH; j++) {
            printf("%c", field[i][j] ? '1' : '0');
        }
        printf("\n");
    }
}

int read_initial_state(int field[HEIGHT][WIDTH]) {
    char line[WIDTH + 2];  // +2 to account for newline and null terminator

    for (int i = 0; i < HEIGHT; i++) {
        if (!fgets(line, sizeof(line), stdin)) {
            return 0;
        }
        for (int j = 0; j < WIDTH; j++) {
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
