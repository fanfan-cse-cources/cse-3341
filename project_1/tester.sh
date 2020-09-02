#!/bin/bash

runner=$1

if test -f main.py
then
	runner="python3.7 main.py"
elif test -f Main.java
then
	echo "Attempting to compile..."
	javac *.java
	runner="java Main"
fi

for value in {1..9}
do
	echo "Running 0${value}.code"
	timeout 5 ${runner} Correct/0${value}.code > Correct/0${value}.student
	echo "Running diff with 0${value}.expected"
	diff -q Correct/0${value}.expected Correct/0${value}.student
done

for value in {0..3}
do
	echo "Running 1${value}.code"
	timeout 5 ${runner} Correct/1${value}.code > Correct/1${value}.student
	echo "Running diff with 1${value}.expected"
	diff -q Correct/1${value}.expected Correct/1${value}.student
done

echo Done!
