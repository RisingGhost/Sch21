import numpy as np


class Node():
    def __init__(self, j, t, left, right, answer = None):
        self.t = t
        self.j = j
        self.left = left
        self.right = right
        self.answer = answer

def split(data):
    l = len(data)//2
    return data[:l], data[l:]


def rec(data, n):
    t = np.random.randint(0,10)
    j = np.random.randint(0,10)
    left, right = split(data)

    if n == 0:
        node_n = Node(j, t, left, right, answer='final')
        return node_n
    

    node_n = Node(j, t, rec(left, n-1), rec(right, n-1))
    return node_n

check = np.arange(40, -1)