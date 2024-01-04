#!/bin/bash

directory="game/src"

files=$(find $directory -type f -name "*.py")

for file in $files
do
	pylint $file --disable=C0301,C0103,E1101

	echo -e "$output\n\033[32m============================================================\033[0m"
done