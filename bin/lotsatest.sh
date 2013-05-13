#!/bin/bash

if [ "$1" == "" ] || [ "$2" == "" ] || [ "$3" == "" ]; then
    echo "Usage:"
    echo "  ./lotsatest.sh TEST_FILE GOAL_SCORE TIMEOUT"
    exit
fi

cd ..
cmd="timeout $3s ./run.py -d tests/$1 ai/random.py"
echo $cmd

rawr() {
    echo `${cmd} | grep "Cycles" | sed -e "s|Cycles: ||"`
}

res="10000000"
while [ "$res" -ge $2 ]; do
    res=`rawr`
    if [ "$res" == "" ]; then
	echo "timeout"
	res="100000000"
    else
	echo "$res"
    fi
done