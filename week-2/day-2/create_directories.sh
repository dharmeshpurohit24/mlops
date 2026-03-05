#!/bin/bash

noOfFiles=10
filename="project_"

for ((fileNo=1;fileNo<=$noOfFiles;fileNo++));do
        $(mkdir "$filename$fileNo")
        echo "$filename$fileNo"
done
