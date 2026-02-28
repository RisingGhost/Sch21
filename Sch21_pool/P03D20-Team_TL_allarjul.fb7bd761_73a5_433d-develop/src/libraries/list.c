#include "list.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

node *elem_init(const char *str) {
    node *init_node = (node *)malloc(sizeof(node));
    if (init_node) {
        init_node->data = (char *)malloc(sizeof(char) * (strlen(str) + 1));
        if (init_node->data) {
            strcpy(init_node->data, str);
            init_node->next = NULL;
        }
    }

    return init_node;
}

node *list_add(list *root, char *str) {
    if (!root || !str) return NULL;

    node *new_node = elem_init(str);
    new_node->next = NULL;

    if (!root->head) {
        root->head = new_node;
        return new_node;
    }

    node *current = root->head;
    while (current->next) {
        current = current->next;
    }
    current->next = new_node;
    return new_node;
}

void list_destroy(list *root) {
    node *current = root->head;
    while (current) {
        node *to_free = current;
        current = current->next;
        free(to_free->data);
        free(to_free);
    }
    free(root);
}

list *list_init() {
    list *lst = (list *)malloc(sizeof(list));
    lst->head = NULL;
    return lst;
}
