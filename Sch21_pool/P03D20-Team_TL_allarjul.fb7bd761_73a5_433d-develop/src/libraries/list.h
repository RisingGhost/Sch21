#ifndef LIST
#define LIST

#include <stdio.h>
#include <string.h>

typedef struct node {
    char *data;
    struct node *next;
} node;

typedef struct list {
    node *head;
} list;

list *list_init();
node *elem_init();
node *list_add(list *elem, char *str);  // в конец списка
void list_destroy(list *root);

#endif