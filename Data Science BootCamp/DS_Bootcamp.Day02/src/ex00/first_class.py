class Must_Read:

    try:
        file = open("data.csv", "r")
        for line in file:
            print(line, end="")
        file.close()
    except Exception:
        raise Exception("can`t open file")


if __name__ == "__main__":
    Must_Read()


# class Must_read:

#     def __init__(self, path):
#         self.path = path
#         file = open(path, "r")
#         for line in file:
#             print(line, end="")
#         file.close()


# if __name__ == "__main__":
#     Must_read("data.csv")
