def sorter():
    list_of_tuples = [
        ("Russia", "25"),
        ("France", "132"),
        ("Germany", "132"),
        ("Spain", "178"),
        ("Italy", "162"),
        ("Portugal", "17"),
        ("Finland", "3"),
        ("Hungary", "2"),
        ("The Netherlands", "28"),
        ("The USA", "610"),
        ("The United Kingdom", "95"),
        ("China", "83"),
        ("Iran", "76"),
        ("Turkey", "65"),
        ("Belgium", "34"),
        ("Canada", "28"),
        ("Switzerland", "26"),
        ("Brazil", "25"),
        ("Austria", "14"),
        ("Israel", "12"),
    ]
    Countries = {}
    for tup in list_of_tuples:
        Countries[tup[0]] = int(tup[1])
    inverted = {}
    for country in Countries:
        if Countries[country] not in inverted:
            inverted[int(Countries[country])] = [country]
        else:
            inverted[int(Countries[country])].append(country)
    for code in sorted(inverted, reverse=True):
        for country in sorted(inverted[code]):
            print(country)


if __name__ == "__main__":
    sorter()
