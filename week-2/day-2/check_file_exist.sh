#!/bin/bash

filename=$1

if [[ -f "$filename" ]];then
        echo "File exist in current dir"
        echo $(stat -c%s "$filename")
else
        echo "File not found"
fi