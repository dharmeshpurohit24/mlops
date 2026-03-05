#!/bin/bash

homeDirPath="/home"
backupDirPath="/backup"

backupDate=$(date -I)

mkdir -p "$backupDirPath"

tar -czf "$backupDirPath/backup_$backupDate.tar.gz" $homeDirPath

echo "Backup completed for $backupDate."