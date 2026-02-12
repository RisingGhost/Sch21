#!/usr/bin/env python3
import os
import subprocess


def checker():
    return os.environ.get("VIRTUAL_ENV")


def installer():
    subprocess.run(["pip", "install", "-r", "requirements.txt"])
    result = subprocess.run(["pip", "freeze"], capture_output=True, text=True).stdout
    print("\n\n", result)
    return result


if __name__ == "__main__":
    if checker() is not None:
        with open("requirements.txt", "a") as file:
            file.write(installer())

    else:
        raise Exception("You are not in vm")
