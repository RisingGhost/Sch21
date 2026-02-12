#!/usr/bin/env python3
# pip install requests
import requests
import sys
from bs4 import BeautifulSoup as bs
import time


def parser(ticker):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    }
    url = f"https://finance.yahoo.com/quote/{ticker}/financials?p={ticker}"

    raw_data = requests.get(url, headers=headers, timeout=5)
    if raw_data.status_code == 200:
        soup = bs(raw_data.text, "html.parser")
        return soup
    else:
        raise Exception(raw_data.status_code)


def function(soup, field):
    field = field.title()
    result_table = {}

    main_rows = soup.find_all("div", class_="row lv-0 yf-t22klz")
    if main_rows == []:
        raise Exception("Wrong Ticker")
    for row in main_rows:
        one_row = row.find_all("div")
        temp_row = []
        [temp_row.append(elem.get_text()) for elem in one_row]
        if temp_row[1] == " ":
            result_table[temp_row[0].strip().title()] = temp_row[3:]
        else:
            result_table[temp_row[0].strip().title()] = temp_row[2:]

    # for row in result_table:
    #     print(row, result_table[row])
    if field in result_table:
        printer = [field.title()]
        [printer.append(elem) for elem in result_table[field]]
    else:
        raise Exception("Bad field")
    # time.sleep(5)
    return tuple(printer)


if __name__ == "__main__":
    try:
        if len(sys.argv) == 3:
            data = parser(sys.argv[1])
            res = function(data, sys.argv[2])
            print(res)
        else:
            raise Exception("invalid input")
    except Exception as e:
        print(e)
