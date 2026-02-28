#!/bin/sh

echo '"name","count"' > hh_uniq_positions.csv

tail -n +2 ../ex03/hh_positions.csv | awk -F',' '{
grade = $3
if (grade ~ /Junior/) i++
if (grade ~ /Middle/) j++
if (grade ~ /Senior/) k++                                                                                       
}                                                                                                              
END {                                                                                                          
print "\"Junior\"," i                                                                                            
print "\"Middle\"," j                                                                                            
print "\"Senior\"," k                                                                                            
}' | sort -t',' -k2,2nr >> hh_uniq_positions.csv 