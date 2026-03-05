#!/bin/bash

threshold=80
partition="/"

diskSpace=$(df -h $partition | awk 'NR==2 {gsub("%",""); print $5}')

if [ "$diskSpace" -ge "$threshold" ];then
  echo "Disk space usage > 80% !" | mail -s "Disk space alert on root in ITT Laptop" root
fi