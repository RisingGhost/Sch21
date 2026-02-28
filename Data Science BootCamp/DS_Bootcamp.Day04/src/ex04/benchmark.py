#!/usr/bin/env python3
import timeit
import random
from collections import Counter


class generator:
    def __init__(self):
        self.list_gen()
        self.dict_gen()
        self.counter_dict_gen()

    def list_gen(self):
        self.list = [random.randint(0, 100) for i in range(1000000)]
        return self.list

    def dict_gen(self):
        d = {elem: 0 for elem in set(self.list)}
        for elem in self.list:
            d[elem] += 1
        self.dict = d
        return d

    def top_ten(self):
        return sorted(self.dict.items(), key=lambda elem: (-elem[1], elem[0]))[:10]

    def counter_dict_gen(self):
        self.counter_dict = Counter(self.list)
        return self.counter_dict

    def counter_top_ten(self):
        self.counter_top = self.counter_dict.most_common(10)
        return self.counter_top

    def time_tester(self, func):
        return timeit.timeit(func, number=100)


if __name__ == "__main__":
    g = generator()

    print(f"my funcion: {g.time_tester(g.dict_gen)}")
    print(f"Counter: {g.time_tester(g.counter_dict_gen)}")
    print(f"my top: {g.time_tester(g.top_ten)}")
    print(f"Counter`s top: {g.time_tester(g.counter_top_ten)}")

    # print("My top ten elements:")
    # [print(f"{elem[0]} -:- {elem[1]}") for elem in g.top_ten()]
    # print("Counter`s top ten elements:")
    # [print(f"{elem[0]} -:- {elem[1]}") for elem in g.counter_top_ten()]
