import sys
from random import randint


class Research:
    def __init__(self, path):
        self.path = path

    def file_reader(self, has_header=True):
        self.has_header = has_header
        try:
            file = open(self.path, "r")
        except FileNotFoundError:
            raise Exception("file not found")
        self.header_reader(file)
        self.data = self.line_reader(file)
        file.close()
        return self.data

    def header_reader(self, file):
        self.header = file.readline()
        if self.header.count(",") == 1:
            l_header = [p.strip() for p in self.header.split(",")]
            if l_header[0] == "" or l_header[1] == "":
                raise Exception("invalid header")
            elif (l_header[0] == "0" and l_header[1] == "1") or (
                l_header[0] == "1" and l_header[1] == "0"
            ):
                self.has_header = False
        else:
            raise Exception("invalid header")

    def line_reader(self, file):
        lines = []
        if self.has_header == False:
            lines.append([int(p.strip()) for p in self.header.split(",")])
        for line in file:
            if line.count(",") == 1:
                left, right = [int(part.strip()) for part in line.split(",")]
                if left == 0 and right == 1:
                    lines.append([left, right])
                elif left == 1 and right == 0:
                    lines.append([left, right])
                else:
                    raise Exception("invalid line")
            else:
                raise Exception("invalid line")
        if not lines:
            raise Exception("there is no lines in file")
        return lines

    class Calculations:
        def __init__(self, data):
            self.data = data
            pass

        def counts(self):
            counter = [int(0), int(0)]
            for elem in self.data:
                if elem[0] == 1:
                    counter[0] += 1
                elif elem[1] == 1:
                    counter[1] += 1
            return counter

        def fractions(self, heads, tails):
            left = heads / (heads + tails) * 100
            right = tails / (heads + tails) * 100
            return [left, right]

    class Analytics(Calculations):
        def predict_random(self, number):
            self.predicted_list = []
            for i in range(number):
                orel = randint(0, 1)
                if orel == 1:
                    reshka = 0
                else:
                    reshka = 1
                self.predicted_list.append([orel, reshka])
            return self.predicted_list

        def predict_last(self):
            return self.data[len(self.data) - 1]


if __name__ == "__main__":
    if len(sys.argv) == 2:
        research = Research(sys.argv[1])
        print(research.file_reader(True))
        calc = Research.Calculations(research.data)
        calc_result = calc.counts()
        print(*calc_result)
        perc = calc.fractions(calc_result[0], calc_result[1])
        print(*perc)
        predict = Research.Analytics(research.data)
        print(predict.predict_random(3))
        print(predict.predict_last())
    else:
        raise Exception("invalid argument count")
