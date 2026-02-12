#!/usr/bin/env python3
import timeit


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

    def time_tester(self, func):
        return timeit.timeit(func, number=900000)


if __name__ == "__main__":

    bench = benchmark()

    result = {
        "loop": bench.time_tester(bench.loop),
        "list comprehension": bench.time_tester(bench.list_comprehension),
        "map": bench.time_tester(bench.map_func),
    }
    sorted_result = sorted(result.items(), key=lambda item: (item[1], item[0]))

    print(f"it is better to use a {sorted_result[0][0]}")
    print(f"{sorted_result[0][1]} vs {sorted_result[1][1]} vs {sorted_result[2][1]}")

    # print(bench.loop())
    # print(bench.list_comprehension())
    # print(bench.map_func())
