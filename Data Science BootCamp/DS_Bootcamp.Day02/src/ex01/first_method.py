class Research:

    def file_reader(self):
        try:
            file = open("data.csv", "r")
            result = []
            for line in file:
                result.append(line)
            file.close()
            return "".join(result)
        except Exception:
            raise Exception("can`t open file")


if __name__ == "__main__":
    print(Research().file_reader(), end="")
