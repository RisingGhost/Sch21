#!/bin/sh

files=$(echo *.csv)

first_or_not=1
for f in $files; do
  if [ "$first_or_not" = 1 ]; then
    head -n1 "$f" > hh_positions.csv
    first_or_not=0
  else
    tail -n +2 "$f" >> hh_positions.csv
  fi
done
