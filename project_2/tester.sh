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
	timeout 5 ${runner} Cases/Correct/0${value}.code > Cases/Correct/0${value}.student
	echo "Running diff with 0${value}.expected"
	diff -q Cases/Correct/0${value}.expected Cases/Correct/0${value}.student
done

for value in {10..26}
do
	echo ""
	echo "Running 0${value}.code"
	timeout 5 ${runner} Cases/Correct/${value}.code > Cases/Correct/${value}.student
	echo "Running diff with ${value}.expected"
	diff -q Cases/Correct/${value}.expected Cases/Correct/${value}.student
done

echo "Running error cases:"
echo ""
echo "Running 01.error:"
timeout 5 ${runner} Cases/Error/01.code Cases/Correct/01.data
read -n 1 -p "Error is ++ in expression. Error message related to that? (y/n)" mainmenuinput
if [ $mainmenuinput = "y" ]; then
	echo -e "\nCorrect aknowledged"
else
	echo -e "\nIncorrect aknowledged"
fi
echo ""
echo "Running 02.error:"
timeout 5 ${runner} Cases/Error/02.code Cases/Correct/02.data
read -n 1 -p "Error is uninitialized variable. Error message related to that? (y/n)" mainmenuinput
if [ $mainmenuinput = "y" ]; then
	echo -e "\nCorrect aknowledged"
else
	echo -e "\nIncorrect aknowledged"
fi
echo ""
echo "Running 03.error:"
timeout 5 ${runner} Cases/Error/03.code Cases/Correct/03.data
read -n 1 -p "Error is variable declared twice. Error message related to that? (y/n)" mainmenuinput
if [ $mainmenuinput = "y" ]; then
	echo -e "\nCorrect aknowledged"
else
	echo -e "\nIncorrect aknowledged"
fi
echo ""
echo "Running 04.error:"
timeout 5 ${runner} Cases/Error/04.code Cases/Correct/04.data
read -n 1 -p "Error is endif missing. Error message related to that? (y/n)" mainmenuinput
if [ $mainmenuinput = "y" ]; then
	echo -e "\nCorrect aknowledged"
else
	echo -e "\nIncorrect aknowledged"
fi
echo ""
echo "Running 05.error:"
timeout 5 ${runner} Cases/Error/05.code Cases/Correct/05.data
read -n 1 -p "Error is == in condition. Error message related to that? (y/n)" mainmenuinput
if [ $mainmenuinput = "y" ]; then
	echo -e "\nCorrect aknowledged"
else
	echo -e "\nIncorrect aknowledged"
fi
echo ""
echo "Running 06.error:"
timeout 5 ${runner} Cases/Error/06.code Cases/Correct/06.data
read -n 1 -p "Error is endif instead of endwhile. Error message related to that? (y/n)" mainmenuinput
if [ $mainmenuinput = "y" ]; then
	echo -e "\nCorrect aknowledged"
else
	echo -e "\nIncorrect aknowledged"
fi
echo ""
echo "Running 07.error:"
timeout 5 ${runner} Cases/Error/07.code Cases/Correct/07.data
read -n 1 -p "Error is ids after end. Error message related to that? (y/n)" mainmenuinput
if [ $mainmenuinput = "y" ]; then
	echo -e "\nCorrect aknowledged"
else
	echo -e "\nIncorrect aknowledged"
fi
echo ""
echo "Running 08.error:"
timeout 5 ${runner} Cases/Error/08.code Cases/Correct/08.data
read -n 1 -p "Error is begin keyword missing. Error message related to that? (y/n)" mainmenuinput
if [ $mainmenuinput = "y" ]; then
	echo -e "\nCorrect aknowledged"
else
	echo -e "\nIncorrect aknowledged"
fi
echo ""
echo "Running 09.error:"
timeout 5 ${runner} Cases/Error/09.code Cases/Correct/09.data
read -n 1 -p "Error is missing semicolon. Error message related to that? (y/n)" mainmenuinput
if [ $mainmenuinput = "y" ]; then
	echo -e "\nCorrect aknowledged"
else
	echo -e "\nIncorrect aknowledged"
fi
echo ""
echo "Running 10.error:"
timeout 5 ${runner} Cases/Error/10.code Cases/Correct/10.data
read -n 1 -p "Error is missing right parenthesis. Error message related to that? (y/n)" mainmenuinput
if [ $mainmenuinput = "y" ]; then
	echo -e "\nCorrect aknowledged"
else
	echo -e "\nIncorrect aknowledged"
fi


echo "Done!"