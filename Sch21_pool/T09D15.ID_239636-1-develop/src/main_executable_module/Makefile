b_src = ../../build
quest_3 = $(b_src)/quest_3

# Список исходных файлов
src_q_3 = ../data_libs/data_io.c ../data_libs/data_stat.c ../data_libs/sort.c ../yet_another_decision_module/decision.c  ../data_module/data_process.c main_executable_module.c

# Промежуточные object-файлы
o_files = $(src_q_3:.c=.o)

# компилятор и флаги
CC = gcc
flags = -std=c11 -Wall -Wextra -Werror

# общая цель
all: $(quest_3)

# Правило сборки исполняемого файла
$(quest_3): $(o_files)
	$(CC) $(flags) -o $(quest_3) $(o_files)

# Правило сборки .o файлов из .c
%.o: %.c
	$(CC) $(flags) -c $< -o $@

# Удаление временных файлов
clean:
	rm -f $(o_files) $(quest_3)
