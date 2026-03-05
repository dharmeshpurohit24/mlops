#!/bin/bash

backupSource="/home/piyush"
backupDestination="./"

date=$(date -I)

backupFilename="backup_$date"

tar -czf "$backupDestination/$backupFilename.tar.gz" "$backupSource"

echo "Backup of $backupSource completed!"