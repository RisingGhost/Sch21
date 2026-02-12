import sys
import os


class Research:
    def __init__(self, path):
        self.path = path
        if not os.path.isfile(path):
            raise Exception("invalid file")

    def file_reader(self):
        try:
            file = open(self.path, "r")
            self.header_reader(file)
            self.line_reader(file)
            result = f"{self.header}{self.lines}"
            file.close()
            return result
        except Exception:
            raise Exception("can`t open file")

    def header_reader(self, file):
        self.header = file.readline()
        if self.header.count(",") == 1:
            l_header = [p.strip() for p in self.header.split(",")]
            if l_header[0] == "" or l_header[1] == "":
                raise Exception("invalid header")
        else:
            raise Exception("invalid header")

    def line_reader(self, file):
        lines = []
        for line in file:
            if line.count(",") == 1:
                left, right = [part.strip() for part in line.split(",")]
                if left == "0" and right == "1":
                    lines.append(line)
                elif left == "1" and right == "0":
                    lines.append(line)
                else:
                    raise Exception("invalid line")
            else:
                raise Exception("invalid line")
        if not lines:
            raise Exception("there is no lines in file")
        self.lines = "".join(lines)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(Research(sys.argv[1]).file_reader(), end="")
    else:
        raise Exception("invalid argument count")
