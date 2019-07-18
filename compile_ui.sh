#!/bin/bash
# Script to compile UI files

for file in datatool/interface/*; do 
    if [[ $file == *.ui ]]
    then
	filename=$(basename -- "$file")
	filename="${filename%.*}"
        pyuic5 -o datatool/interface/$filename.py datatool/interface/$filename.ui
    fi
    if [[ $file == *.qrc ]]
    then
	filename=$(basename -- "$file")
	filename="${filename%.*}"
        pyrcc5 -o ${filename}_rc.py datatool/interface/${filename}.qrc 
    fi
done
