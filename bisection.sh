#!/bin/bash

testdata="testdata4.txt"

script1="challenge6.py"
script2="challenge8.py"
output1="output1.txt"
output2="output2.txt"


lines=`wc -l $testdata | cut -d' ' -f1`
lastdata=$testdata

while [[ $lines -ge 3 ]]; do
    echo "lines: $lines, bodysize: $bodysize, halfsize: $halfsize"
    bodysize=`echo \($lines - 2\) | bc`
    bodysizeplusone=`echo \($lines - 1\) | bc`
    halfbodysize=`echo $bodysize / 2 | bc`
    front="${testdata}-f"
    back="${testdata}-b"
    echo "front: $front, back: $back"
    echo "$halfbodysize 1" > $front
    echo "$halfbodysize 1" > $back
    tail -$bodysizeplusone $testdata | head -$bodysize | \
	head -$halfbodysize >> $front
    tail -1 $testdata >> $front
    tail -$bodysizeplusone $testdata | head -$bodysize | \
	tail -$halfbodysize >> $back
    tail -1 $testdata >> $back

    echo "executing python $script1 < $front > $output1"
    python $script1 < $front > $output1
    echo "executing python $script2 < $front > $output2"
    python $script2 < $front > $output2

    echo "testing output for $front"
    if diff $output1 $output2 ;then
	echo "...match"
	front_error="no"
    else
	echo "...differ"
	front_error="yes"
    fi
    
    echo "executing python $script1 < $back > $output1"
    python $script1 < $back > $output1
    echo "executing python $script2 < $back > $output2"
    python $script2 < $back > $output2

    echo "testing output for $back"
    if diff $output1 $output2 ;then
	echo "...match"
	back_error="no"
    else
	echo "...differ"
	back_error="yes"
    fi

    lastdata=$testdata

    if [[ $front_error == "yes" ]]; then
	testdata=$front
    fi
    
    if [[ $back_error == "yes" ]]; then
	testdata=$back
    fi

    if [[ "$front_error" == "no" && "$back_error" == "no" ]]; then
	echo "minimal data which produces error: $lastdata"
	exit 0
    else
	echo "retrying test with $testdata"
    fi

    lines=`wc -l $testdata | cut -d' ' -f1`
done
    