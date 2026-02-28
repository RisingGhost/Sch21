#!/usr/bin/env python3
import timeit
import sys


class benchmark:
    def __init__(self):
        self.emails = [
            "john@gmail.com",
            "james@gmail.com",
            "alice@yahoo.com",
            "anna@live.com",
            "philipp@gmail.com",
            "john@gmail.com",
            "james@gmail.com",
            "alice@yahoo.com",
            "anna@live.com",
            "philipp@gmail.com",
            "john@gmail.com",
            "james@gmail.com",
            "alice@yahoo.com",
            "anna@live.com",
            "philipp@gmail.com",
            "john@gmail.com",
            "james@gmail.com",
            "alice@yahoo.com",
            "anna@live.com",
            "philipp@gmail.com",
            "john@gmail.com",
            "james@gmail.com",
            "alice@yahoo.com",
            "anna@live.com",
            "philipp@gmail.com",
        ]

    def loop(self):
        result = []
        for email in self.emails:
            if "gmail" in email:
                result.append(email)
        return result

    def list_comprehension(self):
        return [email for email in self.emails if "gmail" in email]

    def map_func(self):
        return list(map(lambda elem: elem if "gmail" in elem else None, self.emails))

    def filter_func(self):
        return list(filter(lambda elem: elem if "gmail" in elem else None, self.emails))

    def time_tester(self, func, num):
        return timeit.timeit(func, number=num)


if __name__ == "__main__":

    try:
        if len(sys.argv) != 3:
            raise Exception("invalid argument number")
        elif sys.argv[1] not in {"loop", "list_comprehension", "map", "filter"}:
            raise Exception("unknown method")

        bench = benchmark()
        method, num = sys.argv[1], int(sys.argv[2])
        if method == "loop":
            print(bench.time_tester(bench.loop, num))
        elif method == "list_comprehension":
            print(bench.time_tester(bench.list_comprehension, num))
        elif method == "map":
            print(bench.time_tester(bench.map_func, num))
        elif method == "filter":
            print(bench.time_tester(bench.filter_func, num))
        else:
            print("unknown method")
    except Exception as e:
        print(f"Error: {e}")
