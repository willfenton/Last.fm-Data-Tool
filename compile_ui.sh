#!/bin/bash
# Script to compile UI files

for file in UI/*; do 
    if [[ $file == *.ui ]]
    then
        filename="${file%.*}"
        pyuic5 -o $filename.py $filename.ui
    fi
done
