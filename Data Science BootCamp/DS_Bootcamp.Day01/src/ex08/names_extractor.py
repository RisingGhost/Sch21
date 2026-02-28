import sys


def function():
    file = open("employees.tsv", "r")
    email = sys.argv[1]
    for line in file:
        if email == line.split("\t")[2].strip():
            return f'Dear {line.split("\t")[0]}, welcome to our team! We are sure that it will be a pleasure to work with you. That’s a precondition for the professionals that our company hires.'
    file.close()


if __name__ == "__main__":
    print(function())
