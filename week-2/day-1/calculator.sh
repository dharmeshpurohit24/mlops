#!/bin/bash

printf "\n"

echo "Basic calculator:-"

read -p "Operator 1: " value1
read -p "Operator 2: " value2

read -p "Enter Operation to perfrom (+,-,*,/,%): " operation

result=-1

case "$operation" in
  "+")
    result=$((value1 + value2))
    ;;
  "-")
    result=$((value1 - value2))
    ;;
  "*")
    result=$((value1 * value2))
    ;;
  "/")
    if [[ "$value2" -ne 0 ]]; then
        result=$((value1 / value2))
    else
        echo "Division by zero not possible"
        exit 1
    fi
    ;;
  "%")
    if [[ "$value2" -ne 0 ]]; then
        result=$((value1 % value2))
    else
        echo "Modulo by zero not possible"
        exit 1
    fi
    ;;
  *)
    echo "Invalid operation"
    exit 1
    ;;
esac

echo "Result: $result"
