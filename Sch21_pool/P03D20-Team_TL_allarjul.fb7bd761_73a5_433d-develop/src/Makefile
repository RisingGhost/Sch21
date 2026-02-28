CC = gcc
CFLAGS = -c -Wall -Werror -Wextra -std=c11
SOURCES = graph.c ./libraries/list.c ./libraries/stack_double.c ./libraries/stack.c ./modules/parser.c ./modules/print.c ./modules/translate_and_calculate.c ./modules/types.c
OBJECTS = $(BUILD)graph.o $(BUILD)list.o $(BUILD)stack_double.o $(BUILD)stack.o $(BUILD)parser.o $(BUILD)print.o $(BUILD)translate_and_calculate.o $(BUILD)types.o 
BUILD = ../build/
EXECUTABLE = $(BUILD)graph

.PHONY: all clean rebuild 

all: $(SOURCES) $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS)
	$(CC) $(OBJECTS) -o $@ -lm

clean:
	rm -rf $(OBJECTS) $(EXECUTABLE)

rebuild: clean all

$(BUILD)%.o: modules/%.c
	$(CC) $(CFLAGS) $< -o $@

$(BUILD)%.o: libraries/%.c
	$(CC) $(CFLAGS) $< -o $@

$(BUILD)%.o: %.c
	$(CC) $(CFLAGS) $< -o $@

clang:
	clang-format -i libraries/* modules/* *.c

leaks:
	leaks -atExit -- ../build/graph

run: all
	../build/graph