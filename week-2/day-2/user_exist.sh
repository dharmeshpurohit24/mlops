#!/bin/bash

read -p "Enter a username: " username

output=$(getent passwd "$username")

if [ -n "$output" ];then
        echo "User exist!"
else
        echo "User doesn't exist!"
fi

