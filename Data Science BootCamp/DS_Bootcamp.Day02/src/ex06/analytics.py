from random import randint
import logging
import requests

logging.basicConfig(
    level=logging.INFO,
    filename="analytics.log",
    format="%(asctime)s %(message)s",
)


class Research:
    def __init__(self, path):
        self.path = path
        logging.info("Research init")

    def file_reader(self, has_header):
        self.has_header = has_header
        try:
            file = open(self.path, "r")
        except FileNotFoundError:
            logging.info("file not found")
            raise Exception("file not found")
        self.header_reader(file)
        self.data = self.line_reader(file)
        file.close()
        logging.info(f"file reading completed")
        return self.data

    def header_reader(self, file):
        if self.has_header == True:
            self.header = file.readline()
            if self.header.count(",") == 1:
                l_header = [p.strip() for p in self.header.split(",")]
                if l_header[0] == "" or l_header[1] == "":
                    logging.info("finvalid header")
                    raise Exception("invalid header")
            else:
                logging.info(f"invalid header")
                raise Exception("invalid header")
        logging.info(f"header check success")

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
                    logging.info("invalid line")
                    raise Exception("invalid line")
            else:
                logging.info("invalid line")
                raise Exception("invalid line")

        if not lines:
            logging.info("there is no lines in file")
            raise Exception("there is no lines in file")
        logging.info(f"lines in file were successfully read")
        return lines

    def message_sender(self, chat_id, bot_token, flag):
        if flag == True:
            text = "The report has been successfully created"
        else:
            text = "The report hasn't been created due to an error."
        try:
            requests.post(
                f"https://api.telegram.org/bot{bot_token}/sendMessage",
                json={"chat_id": chat_id, "text": text},
            )
            logging.info("message was successfully send")
        except Exception:
            logging.info("message was not send")
            raise Exception("message was not send")

    class Calculations:
        def __init__(self, data):
            self.data = data
            logging.info("Calculations init")

        def counts(self):
            counter = [int(0), int(0)]
            for elem in self.data:
                if elem[0] == 1:
                    counter[0] += 1
                elif elem[1] == 1:
                    counter[1] += 1
                self.heads, self.tails = counter[0], counter[1]
            logging.info(
                f"Calculating the counts of heads and tails heads={counter[0]} tails={counter[1]}"
            )
            return counter

        def fractions(self, heads, tails):
            self.left = heads / (heads + tails) * 100
            self.right = tails / (heads + tails) * 100
            logging.info(
                f"calculated percents of heads and tails heads={self.left:.2f} tails={self.right:.2f}"
            )
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
            logging.info(f"Predicted {number} rolls successfully")
            return self.predicted_list

        def predict_last(self):
            logging.info("predicted last successfully")
            return self.data[len(self.data) - 1]

        def save_file(self, data, file_name, extension):
            file = open(f"{file_name}.{extension}", "w")
            file.write(data)
            file.close()
            logging.info(f"saved file to {file_name}.{extension} successfully")
