import requests
import re
from collections import Counter
from bs4 import BeautifulSoup as bs
import os


class Links:
    """
    Analyzing data from links.csv
    """

    def __init__(self, path_to_the_file):
        try:
            print("Links class initialization...")
            self.file_reader(path_to_the_file)
            self.dataset_path = "ex_links.tsv"
            if not os.path.isfile(self.dataset_path):
                self.data_exists = False
                self.error = "Вы не скачали наш датасет, скачайте или создайте свой"
                raise Exception(self.error)
            else:
                self.data_exists = True
                self.dict_from_data()
        except Exception as e:
            print(e)
        # [print(k, v) for k, v in self.ex_links_dict.items()]

    def file_reader(self, path_to_the_file):
        if not os.path.isfile(path_to_the_file):
            raise Exception("добавьте файл links.csv")
        else:
            self.links_dict = {}
            file = open(path_to_the_file, "r")
            header = file.readline()
            self.links_dict = {
                line.split(",")[0]: [elem.strip() for elem in line.split(",")[1:]]
                for line in file
            }
            file.close()
            return self.links_dict

    def dict_from_data(self):
        if not self.data_exists:
            print(self.error)
        else:
            print(f"'{self.dataset_path}' initialization...")
            ex_links_dict = {}
            with open(self.dataset_path, "r", encoding="utf-8") as data:
                header_skip = data.readline()
                for line in data:
                    splitted = line.split("\t")
                    ex_links_dict.update({splitted[0]: splitted[1:]})
            self.ex_links_dict = ex_links_dict
            print("successfully initialized\nNow cleaning...")
            if len(header_skip.split("\t")) > 9:
                for k, v in self.ex_links_dict.items():
                    v[4] = self.Cleaner.clean_budget(v[4])
                    v[5] = self.Cleaner.clean_budget(v[5])
                    v[3] = self.Cleaner.clean_time(v[3])
                self.flag = True
            else:
                self.flag = False
                self.error = "Столбцов в датасете не верное кол-во."
            print("You can call all methods now")

    def get_imdb(self, list_of_movies, list_of_fields):
        import time

        def parse(imdb_id, list_of_fields):
            headers = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            }
            all_fields = {
                "title": "h1[data-testid='hero__pageTitle'], h1[data-testid='hero-title-block__title']",
                "director": "li.ipc-metadata-list__item:has(span:-soup-contains('Director')) a",
                "release_date": "li[data-testid='title-details-releasedate'] a",
                "runtime": "li[data-testid='title-techspec_runtime'] div ul li",
                "budget": "li[data-testid='title-boxoffice-budget'] > div > ul > li > span:last-child",
                "cumulative_gross": "li[data-testid='title-boxoffice-cumulativeworldwidegross'] > div > ul > li > span:last-child",
                "production_companies": "li[data-testid='title-details-companies'] li a",
                "countries_of_origin": "li[data-testid='title-details-origin'] li a",
                "languages": "li[data-testid='title-details-languages'] li a",
            }
            fields = {
                field: selector
                for field, selector in all_fields.items()
                if field in list_of_fields
            }
            if not fields:
                raise ValueError("No valid fields to parse.")
            for attempt in range(5):
                try:
                    html = requests.get(
                        f"https://www.imdb.com/title/tt{imdb_id}/", headers=headers
                    )
                    time.sleep(0.01)
                    html.raise_for_status()
                    soup = bs(html.text, "html.parser")

                    data = {}
                    for key, selector in fields.items():
                        items = soup.select(selector)
                        data[key] = list(
                            set(
                                [i.get_text(strip=True) for i in items]
                                if items
                                else ["No Data"]
                            )
                        )
                    return data

                except Exception as e:
                    print(f"\n[{imdb_id}] Ошибка при парсинге ({attempt + 1}/{5}): {e}")
                    time.sleep(7)
                    if attempt == 4:
                        return {field: ["No Data"] for field in fields}

        imdb_info = []
        list_of_movies = [
            str(elem)
            for elem in sorted(list_of_movies, reverse=True)
            if str(elem) in self.links_dict.keys()
        ]
        for movie_id in list_of_movies:
            imdb_id = self.links_dict[movie_id][0]
            imdb_info.extend(
                [[movie_id]] + [v for v in parse(imdb_id, list_of_fields).values()]
            )
        # [print(*elem, end="\n\n") for elem in imdb_info]
        # print(f"function print \t {imdb_info}")
        # print(imdb_info)
        return imdb_info

        """
        The method returns a list of lists [movieId, field1, field2, field3, ...] for the list of movies given as the argument (movieId).
                For example, [movieId, Director, Budget, Cumulative Worldwide Gross, Runtime].
                The values should be parsed from the IMDB webpages of the movies.
             Sort it by movieId descendingly.
        """

    def top_directors(self, n):
        if not self.data_exists or not self.flag:
            print(self.error)
        else:
            counts = Counter(v[1] for v in self.ex_links_dict.values())
            temp_sort = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
            sorted_counts = {e[0]: e[1] for e in temp_sort if e[0] != "No Data"}
            """
            The method returns a dict with top-n directors where the keys are directors and
            the values are numbers of movies created by them. Sort it by numbers descendingly.
            """
            if n > 0:
                directors = dict(list(sorted_counts.items())[:n])
            else:
                raise ValueError("n must be > 0")
            return directors

    def most_expensive(self, n):
        if not self.data_exists or not self.flag:
            print(self.error)
        else:
            d = self.ex_links_dict
            sorted_d = sorted(
                d.items(), key=lambda item: ((item[1][4] or 0), item[0]), reverse=True
            )
            budgets = {v[0]: f"${v[4]}" for k, v in sorted_d if v[4] is not None}

            """
            The method returns a dict with top-n movies where the keys are movie titles and
            the values are their budgets. Sort it by budgets descendingly.
            """
            if n > 0:
                budgets = dict(list(budgets.items())[:n])
            return budgets

    def most_profitable(self, n):
        if not self.data_exists or not self.flag:
            print(self.error)
        else:
            d = self.ex_links_dict

            profits = {}
            for title, v in d.items():
                if len(v) > 5 and v[4] is not None and v[5] is not None:
                    profits[v[0]] = v[5] - v[4]

            sorted_profits = dict(
                sorted(profits.items(), key=lambda x: x[1], reverse=True)
            )
            budgets = {k: f"${v}" for k, v in sorted_profits.items()}
            """
            The method returns a dict with top-n movies where the keys are movie titles and
            the values are the difference between cumulative worldwide gross and budget.
            Sort it by the difference descendingly.
            """
            return dict(list(budgets.items())[:n])

    def longest(self, n):
        if not self.data_exists or not self.flag:
            print(self.error)
        else:
            d = self.ex_links_dict
            sorted_d = sorted(
                d.items(), key=lambda item: ((item[1][3] or 0), item[0]), reverse=True
            )
            runtimes = {v[0]: f"{v[3]} mins" for k, v in sorted_d if v[3] is not None}

            """
            The method returns a dict with top-n movies where the keys are movie titles and
            the values are their runtime. If there are more than one version – choose any.
            Sort it by runtime descendingly.
            """
            if n > 0:
                runtimes = dict(list(runtimes.items())[:n])

            return runtimes

    def top_cost_per_minute(self, n):
        if not self.data_exists or not self.flag:
            print(self.error)
        else:
            d = self.ex_links_dict

            costs = {}
            for title, v in d.items():
                if len(v) > 5 and v[3] not in (None, 0) and v[4] is not None:
                    costs[v[0]] = round(v[4] / v[3], 2)

            sorted_costs = dict(sorted(costs.items(), key=lambda x: x[1], reverse=True))
            """
                    The method returns a dict with top-n movies where the keys are movie titles and
            the values are the budgets divided by their runtime. The budgets can be in different currencies – do not pay attention to it.
                The values should be rounded to 2 decimals. Sort it by the division descendingly.
            """
            return dict(list(sorted_costs.items())[:n])

    def create_dataset(self, list_of_movies, list_of_fields):
        print("Введите название вашего датасета:")
        self.dataset_path = f"{input()}.tsv"
        list_of_fields = [
            field.lower()
            for field in list_of_fields
            if field
            in [
                "title",
                "director",
                "release_date",
                "runtime",
                "budget",
                "cumulative_gross",
                "production_companies",
                "countries_of_origin",
                "languages",
            ]
        ]
        [
            print(f"movieId {movie_id} not in links.csv")
            for movie_id in list_of_movies
            if str(movie_id) not in self.links_dict.keys()
        ]
        with open(self.dataset_path, "w", encoding="utf-8") as out:
            out.write(f"movieId\t{'\t'.join(list_of_fields)}\n")
            for key in sorted(list_of_movies, reverse=True):
                result = self.get_imdb([key], list_of_fields)

                s_result = "\t".join(
                    ",".join(str(item).strip() for item in sublist)
                    for sublist in result
                )
                if s_result:
                    out.write(s_result + "\n")

                print(key, end=", ")
            self.data_exists = True
            print(f"\nDataset '{self.dataset_path}' created successfull")

    class Cleaner:
        @staticmethod
        def clean_budget(value):

            if not value or value == "No Data":
                return None
            if not isinstance(value, str):
                return value
            if (
                "$" not in value
                and "usd" not in value.lower()
                and "dollar" not in value.lower()
            ):
                return None

            match = re.search(r"[\d,]+(?:\.\d+)?", value)
            if not match:
                return None

            number_str = match.group(0).replace(",", "")
            try:
                return int(float(number_str))
            except ValueError:
                return None

        @staticmethod
        def clean_time(value):

            if not value or not isinstance(value, str):
                return None
            match = re.search(r"\((\d+)\s*min\)", value)
            if match:
                return int(match.group(1))
            h = m = 0
            if "h" in value:
                h_match = re.search(r"(\d+)\s*h", value)
                if h_match:
                    h = int(h_match.group(1))
            if "m" in value:
                m_match = re.search(r"(\d+)\s*m", value)
                if m_match:
                    m = int(m_match.group(1))
            total = h * 60 + m
            return total if total > 0 else None


if __name__ == "__main__":
    linker = Links("links.csv")
