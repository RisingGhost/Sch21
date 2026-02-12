import sys


def main_function():
    if len(sys.argv) != 4:
        raise Exception("invalid argument count")
    else:
        mode, string, shift = sys.argv[1], sys.argv[2], int(sys.argv[3])

    if mode == "decode":
        shift = -shift
    elif mode != "encode":
        raise Exception("Unknown mode")

    for ch in string:
        if ("а" <= ch <= "я") or ("А" <= ch <= "Я") or (ch in "Ёё"):
            raise Exception("The script does not support your language yet.")

    ch_list = []
    for ch in string:
        ch_list.append(letter_transform(ch, shift))

    print("".join(ch_list))


def letter_transform(ch, shift):
    if "a" <= ch <= "z":
        return chr((ord(ch) - ord("a") + shift) % 26 + ord("a"))
    elif "A" <= ch <= "Z":
        return chr((ord(ch) - ord("A") + shift) % 26 + ord("A"))
    else:
        return ch


if __name__ == "__main__":
    main_function()
