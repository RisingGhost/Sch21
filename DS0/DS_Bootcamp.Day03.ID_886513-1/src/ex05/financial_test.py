#!/usr/bin/env python3
import requests
import sys
from bs4 import BeautifulSoup
import pytest


def parser(ticker):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    }
    url = f"https://finance.yahoo.com/quote/{ticker}/financials?p={ticker}"

    raw_data = requests.get(url, headers=headers, timeout=5)
    if raw_data.status_code == 200:
        soup = BeautifulSoup(raw_data.text, "html.parser")
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

    if field in result_table:
        printer = [field.title()]
        [printer.append(elem) for elem in result_table[field]]
    else:
        raise Exception("Bad field")
    return tuple(printer)


def test_parser1():
    assert isinstance(parser("MSFT"), BeautifulSoup)


def test_parser2():
    assert isinstance(parser("AAPL"), BeautifulSoup)


def test_parser3():
    assert isinstance(parser("wrong_ticker"), BeautifulSoup)


def test_function_tuple():
    assert isinstance(function(parser("MSFT"), "Total Revenue"), tuple)


def test_function_exception():
    with pytest.raises(Exception, match="Wrong Ticker"):
        function(parser("bbabrabrbarbarb"), "Total Revenue")


def test_function_isnone():
    assert function(parser("MSFT"), "Total Revenue") is not None


if __name__ == "__main__":
    try:
        if len(sys.argv) == 3:
            data = parser(sys.argv[1])
            # print(type(data))
            res = function(data, sys.argv[2])
            print(res)
        else:
            raise Exception("invalid input")
    except Exception as e:
        print(e)
