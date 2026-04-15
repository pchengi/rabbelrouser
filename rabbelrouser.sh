#!/bin/bash

wordlist=$1

if [ "$wordlist" = "" ]; then
    echo "Required argument: filtered word-list with the possible words."
    exit -1;
fi
if [ ! -s $wordlist ]; then 
    echo "Provided wordlist $wordlist is not a non-empty file!"
    exit -1;
fi

python sv-eng/dictops.py -e -b -i $wordlist -s
