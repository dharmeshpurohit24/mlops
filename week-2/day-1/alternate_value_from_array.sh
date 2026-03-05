#!/bin/bash


array=(1 2 3 4 5 6 7 8 9 10)

printf "\n"
echo "Current value in array:-"

for value in "${array[@]}";do
        printf "$value "
done

printf "\n\n"
echo "Alternate value from array"

index=0
for value in "${array[@]}";do
        if (( index%2 == 0 ));then
                echo "$value"
        fi
        ((index++))
done
