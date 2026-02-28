def data_types():
    i, s, f, b = 1, "string", 3.14, True
    l, d, t, m = [1, 2], {"key": "clown"}, (1, 2), {1, 2}

    types_list = [i, s, f, b, l, d, t, m]
    for i in range(len(types_list)):
        types_list[i] = type(types_list[i]).__name__
    print(f"[{', '.join(types_list)}]")


if __name__ == "__main__":
    data_types()
