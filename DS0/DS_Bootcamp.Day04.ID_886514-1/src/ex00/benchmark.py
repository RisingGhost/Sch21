#!/usr/bin/env python3
import timeit


def loop(emails):
    result = []
    for email in emails:
        if "gmail" in email:
            result.append(email)
    return result


def list_comprehension(emails):
    return [email for email in emails if "gmail" in email]


if __name__ == "__main__":
    emails = [
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
    n = 90000000
    time_loop = timeit.timeit(lambda: loop(emails), number=n)
    time_comprehension = timeit.timeit(lambda: list_comprehension(emails), number=n)
    result = {"loop": time_loop, "list comprehension": time_comprehension}
    if time_loop < time_comprehension:
        winner, loser = "loop", "list comprehension"
    else:
        winner, loser = "list comprehension", "loop"
    print(f"it is better to use a {winner}")
    print(f"{result[winner]} vs {result[loser]}")
