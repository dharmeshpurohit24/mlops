#!/bin/bash


readWritePermissionToFile(){
  if [ $# -ne 1 ];then
    echo "Function have no arguments"
    return 1
  fi

  local filename="$1"

  if [ ! -f "$filename" ];then
    echo "File dosen't exist!"
    exit 1
  fi

  chmod u+rw "$filename"
}

read -p "Provide filename to set read & write permission for owner: " filename

readWritePermissionToFile "$filename"