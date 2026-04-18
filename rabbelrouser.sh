#!/bin/bash
echo -n >rabinout
while read ln; do
    if [ "$ln" = "--EOF--" ]; then
        break;
    fi
    echo "$ln" >>rabinout
done <"${1:-/dev/stdin}"

if [ ! -s $wordlist ]; then 
    echo "Provided wordlist $wordlist is not a non-empty file!"
    exit -1;
fi

python sv-eng/dictops.py -e -m -i rabinout -s
rm -f rabinout
