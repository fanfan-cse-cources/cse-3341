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
	echo ""
	echo "Running 0${value}.code"
	timeout 5 ${runner} Cases/Correct/0${value}.code Cases/Correct/0${value}.data > Cases/Correct/0${value}.student
	echo "Running diff with 0${value}.expected"
	diff -q Cases/Correct/0${value}.expected Cases/Correct/0${value}.student
done

for value in {10..26}
do
	echo ""
	echo "Running 0${value}.code"
	timeout 5 ${runner} Cases/Correct/${value}.code Cases/Correct/${value}.data > Cases/Correct/${value}.student
	echo "Running diff with ${value}.expected"
	diff -q Cases/Correct/${value}.expected Cases/Correct/${value}.student
done

echo "Running error cases:"
echo ""
echo "Running 01.error:"
timeout 5 ${runner} Cases/Error/01.code Cases/Error/01.data
read -n 1 -p "Error is .data file not having enough values. Error message related to that? (y/n)" mainmenuinput
if [ $mainmenuinput = "y" ]; then
	echo -e "\nCorrect aknowledged"
else
	echo -e "\nIncorrect aknowledged"
fi
echo ""
echo "Running 02.error:"
timeout 5 ${runner} Cases/Error/02.code Cases/Error/02.data
read -n 1 -p "Error is uninitialized variable. Error message related to that? (y/n)" mainmenuinput
if [ $mainmenuinput = "y" ]; then
	echo -e "\nCorrect aknowledged"
else
	echo -e "\nIncorrect aknowledged"
fi


echo "Done!"