import sys


def all_stocks():
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
        s = [word.strip() for word in sys.argv[1].split(",")]
        for cheker in s:
            if cheker == "":
                return
        for elem in s:
            tckr, company = elem.upper(), elem.title()
            if tckr in COMPANIES.values():
                for comp in COMPANIES:
                    if tckr == COMPANIES[comp]:
                        print(tckr, "is a ticker symbol for", comp)
                        break
            elif company in COMPANIES:
                print(company, "stock price is", STOCKS[COMPANIES[company]])
            else:
                print(elem, "is an unknown company or an unknown ticker symbol")


if __name__ == "__main__":
    all_stocks()
