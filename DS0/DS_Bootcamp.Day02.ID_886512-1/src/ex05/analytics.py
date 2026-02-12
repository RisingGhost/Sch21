from random import randint


class Research:
    def __init__(self, path):
        self.path = path

    def file_reader(self, has_header):
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
        if self.has_header == True:
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

        def counts(self):
            counter = [int(0), int(0)]
            for elem in self.data:
                if elem[0] == 1:
                    counter[0] += 1
                elif elem[1] == 1:
                    counter[1] += 1
                self.heads, self.tails = counter[0], counter[1]
            return counter

        def fractions(self, heads, tails):
            self.left = heads / (heads + tails) * 100
            self.right = tails / (heads + tails) * 100
            return [self.left, self.right]

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

        def save_file(self, data, file_name, extension):
            file = open(f"{file_name}.{extension}", "w")
            file.write(data)
            file.close()
