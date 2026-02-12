#!/bin/sh

head -n1 ../ex02/hh_sorted.csv > hh_positions.csv
tail -n +2 ../ex02/hh_sorted.csv | awk -F',' '{
    grade = ""
    if ($3 ~ /Junior/) 
    {
        if (grade == "") { grade = "Junior" } 
        else { grade = grade "/Junior" }
    }
    if ($3 ~ /Middle/) 
    {
        if (grade == "") { grade = "Middle" } 
        else { grade = grade "/Middle" }
    }
    if ($3 ~ /Senior/) 
    {
        if (grade == "") { grade = "Senior" } 
        else { grade = grade "/Senior" }
    }
    if (grade == "") grade = "-"                  
    print $1 "," $2 ",\"" grade "\"," $4 "," $5  
    }' >> hh_positions.csv