#!/usr/bin/env python3
import os


def printer():
    print(f"Your current virtual env is {os.environ.get("VIRTUAL_ENV")}")


if __name__ == "__main__":
    printer()
