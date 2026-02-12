#include "translate_and_calculate.h"

#include <math.h>

#include "../libraries/list.h"
#include "types.h"

int operation_priority(char ch) {
    int priority = 4;
    if (ch == '(' || ch == ')')
        priority = 0;
    else if (ch == '+' || ch == '-')
        priority = 1;
    else if (ch == '*' || ch == '/')
        priority = 2;
    else if (ch == '~')
        priority = 2;
    else if (is_special_function(ch))
        priority = 3;
    return priority;
}

int is_good_input(list *str) {
    node *current = str->head, *prev = NULL;
    int error = 0, balance = 0;
    for (; current != NULL && error != 1; prev = current, current = current->next) {
        char *current_data = current->data;
        if (prev == NULL && ((is_operator(*current_data) && *current_data != '~') || *current_data == ')'))
            error = 1;  // случай первого элемента и первый не может быть оператором

        else if (current->next == NULL && is_operator(*current_data))
            error = 1;

        else if (is_digit(*current_data) || *current_data == 'x') {
            if (prev != NULL && (is_digit(*(prev->data)) || *(prev->data) == 'x')) error = 1;
        } else if (*current_data == '~') {
            if (is_operator(*(current->next->data))) error = 1;
        } else if (is_operator(*current_data)) {
            if (is_operator(*(prev->data)) || *(prev->data) == '(') error = 1;
        } else if (is_special_function(*current_data)) {
            if (current->next != NULL && *(current->next->data) != '(') error = 1;
        } else if (*current_data == '(') {
            balance += 1;
            if (prev != NULL && (balance <= 0 || is_digit(*(prev->data)) || *(prev->data) == 'x')) error = 1;
        } else if (*current_data == ')') {
            balance -= 1;
            if (balance < 0 || *(prev->data) == '(' || is_operator(*(prev->data)) ||
                is_special_function(*(prev->data)))
                error = 1;
        }
    }
    if (balance != 0) error = 1;
    return error;
}

void process_operators(stack *stack_operands, list *res, char *current_data, char *buf_stack,
                       const int *error, int *end) {
    while (*end != 1 && *error != 1 && pop(stack_operands, buf_stack)) {
        if (operation_priority(*current_data) <= operation_priority(*buf_stack)) {
            list_add(res, buf_stack);
        } else {
            *end = 1;
            push(stack_operands, *buf_stack);
        }
    }
}

void process_parentheses(stack *stack_operands, list *res, char *buf_stack, const int *error, int *end) {
    while (*end != 1 && *error != 1 && pop(stack_operands, buf_stack)) {
        if (*buf_stack != '(') {
            list_add(res, buf_stack);
        } else {
            *end = 1;
        }
    }
}

int to_polish_notation(list *str, list *res) {
    node *current = str->head;
    char *buf_stack = (char *)malloc(sizeof(char));
    int error = is_good_input(str);
    stack *stack_operands = init();

    for (; current != NULL && error != 1; current = current->next) {
        int end = 0;
        char *current_data = current->data;
        if (is_digit(*current_data) || *current_data == 'x') {
            list_add(res, current_data);
        } else if ((is_operator(*current_data) || is_special_function(*current_data))) {
            process_operators(stack_operands, res, current_data, buf_stack, &error, &end);
            push(stack_operands, *current_data);
        } else if (*current_data == '(') {
            push(stack_operands, *current_data);
        } else if (*current_data == ')') {
            process_parentheses(stack_operands, res, buf_stack, &error, &end);
        }
    }
    while (pop(stack_operands, buf_stack)) {
        list_add(res, buf_stack);
    }
    free(buf_stack);
    destroy(stack_operands);

    return error != 1;
}

double calculate_expression(list *lst, double x) {
    stack_double *st = init_double();
    node *cur = lst->head;
    double res, calculated_value = 0;
    while (cur) {
        if (is_digit(cur->data[0])) {
            double value = atof(cur->data);
            push_double(st, value);
        } else if (strcmp(cur->data, "x") == 0) {
            double value = x;
            push_double(st, value);
        } else if (is_operator(cur->data[0]) && cur->data[1] == '\0') {
            if (cur->data[0] == '~') {
                double num;
                pop_double(st, &num);
                num = -num;
                push_double(st, num);
            } else {
                double second, first;
                pop_double(st, &second);
                pop_double(st, &first);
                res = calculate_operator(first, second, cur->data[0]);
                push_double(st, res);
            }
        } else if (is_special_function(cur->data[0])) {
            double arg;
            pop_double(st, &arg);
            res = calculate_func(arg, cur->data[0]);

            push_double(st, res);
        }
        cur = cur->next;
    }
    pop_double(st, &calculated_value);
    destroy_double(st);
    return calculated_value;
}

double calculate_operator(double first, double second, char operator) {
    double value = 0;
    switch (operator) {
        case '+':
            value = first + second;
            break;
        case '-':
            value = first - second;
            break;
        case '*':
            value = first * second;
            break;
        case '/':
            value = first / second;
    }

    return value;
}

double calculate_func(double arg, char func) {
    double value = 0;
    switch (func) {
        case 's':
            value = sin(arg);
            break;
        case 'c':
            value = cos(arg);
            break;
        case 't':
            value = tan(arg);
            break;
        case 'q':
            value = sqrt(arg);
            break;
        case 'g':
            value = 1.0 / tan(arg);
            break;
        case 'l':
            value = log(arg);
            break;
    }

    return value;
}
