import sys


def ticker():
    COMPANIES = {
        "Apple": "AAPL",
        "Microsoft": "MSFT",
        "Netflix": "NFLX",
        "Tesla": "TSLA",
        "Nokia": "NOK",
    }

    STOCKS = {
        "AAPL": 287.73,
        "MSFT": 173.79,
        "NFLX": 416.90,
        "TSLA": 724.88,
        "NOK": 3.37,
    }

    if len(sys.argv) == 2:
        tckr = sys.argv[1].upper()
        if tckr in STOCKS:
            for company in COMPANIES:
                if COMPANIES[company] == tckr:
                    print(company, end=" ")
                    break
            print(STOCKS[tckr])
        else:
            print("Unknown ticker")


if __name__ == "__main__":
    ticker()
