#!/usr/bin/env python3
import sys
import resource


def file_reader(path):
    with open(path, "r") as file:
        for line in file:
            yield line


def usage_check():
    usage = resource.getrusage(resource.RUSAGE_SELF)
    print(f"Peak Memory Usage = {usage.ru_maxrss/(1024**2):.3f} GB")
    print(f"User Mode Time + System Mode Time = {usage.ru_utime+usage.ru_stime}s")


if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            raise IndexError("invalid argument count, write only path")
        data = file_reader(sys.argv[1])
        for elem in data:
            pass
        usage_check()
    except Exception as e:
        print(f"error: {e}")
