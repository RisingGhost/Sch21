#!/usr/bin/env python3
from functools import reduce
import sys
import timeit


class math:
    def __init__(self, t_num, s_num):
        self.t_num = t_num
        self.s_num = s_num

    def loop(self):
        sum = 0
        for i in range(self.s_num):
            sum = sum + i * i
        return sum

    def reduce_func(self):
        return reduce(lambda sum, x: sum + x**2, range(self.s_num))

    def time_tester(self, func):
        return timeit.timeit(func, number=self.t_num)


if __name__ == "__main__":

    try:
        if len(sys.argv) != 4:
            raise Exception("invalid argument number")
        elif sys.argv[1] not in {"loop", "reduce"}:
            raise Exception("unknown method")

        method = sys.argv[1]
        s_num = int(sys.argv[3]) + 1
        t_num = int(sys.argv[2])
        m = math(t_num, s_num)
        if method == "loop":
            # print(m.loop())
            print(m.time_tester(m.loop))
        elif method == "reduce":
            # print(m.reduce_func())
            print(m.time_tester(m.reduce_func))
    except Exception as e:
        print(f"error: {e}")
