#!/bin/sh

hdr=$(head -n1 ../ex03/hh_positions.csv)

tail -n +2 ../ex03/hh_positions.csv | awk -F',' '
  {
    created_at = $2
    gsub(/"/, "", created_at)
    gsub(/T.*/, "", created_at)
    filename = created_at ".csv"
    print $0 >> filename
  }
'

for file in *.csv; do
  echo "$hdr" > tmp.csv
  cat "$file" >> tmp.csv
  mv tmp.csv "$file"
done
