def read_n_write():
    ds_csv = open("../../datasets/ds.csv", "r")
    ds_tsv = open("ds.tsv", "w")
    for line in ds_csv:
        opened = 0
        for i in range(len(line)):
            if line[i] == '"' and opened == 0:
                opened = 1
            elif line[i] == "," and opened == 1:
                line2 = line[:i] + "^" + line[i + 1 :]
                line = line2
            elif line[i] == '"' and opened == 1:
                opened = 0

        s = "\t".join(line.split(",")).replace("^", ",")
        ds_tsv.write(s)
    ds_csv.close()
    ds_tsv.close()


if __name__ == "__main__":
    read_n_write()
