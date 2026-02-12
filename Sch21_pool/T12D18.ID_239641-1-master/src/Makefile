CC = gcc
flags = -Wall -Wextra -Werror
c_src = print_module.c main_module.c #documentation_module.c 
b_src = ../build
q1_src = $(b_src)/Quest_1

all : quest_1

quest_1 : 
	$(CC) $(flags) $() -o $(q1_src)

%.o: %.c
	$(CC) $(flags) -c $< -o $@