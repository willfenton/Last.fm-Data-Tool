#!/bin/bash
# Script to compile UI files

for file in qtdesigner/*; do 
    if [[ $file == *.ui ]]
    then
	filename=$(basename -- "$file")
	filename="${filename%.*}"
        pyuic5 -o datatool/interface/$filename.py qtdesigner/$filename.ui
    fi
done
