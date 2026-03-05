#!/bin/bash

logfile="access.log"

if [ ! -f "$logfile" ];then
  echo "log file dosent exist in path $logfile"
  echo "creating one..."

  touch "$logfile"

  for ((data=1; data<=100; data++));do
    echo "128.29.32.$((RANDOM%5+1)) - - [20/Jan/2026:10:00:$((data%60))] \"GET /index.html HTTP/1.1\" 200 1234"
  done >> "$logfile"
fi

echo "Top 5 most frequent Ip address:-"
awk '{print $1}' "$logfile" | sort | uniq -c | sort -nr | head -5