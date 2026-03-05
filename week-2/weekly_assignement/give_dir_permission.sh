#!/bin/bash


readPermissionToDir() {
  if [ $# -ne 1 ];then
    echo "Function have no arg"
    return 1
  fi

  local dirname=$1

  if [ ! -d "$dirname" ];then
    echo "Dir does not exist!"
    exit 1
  fi

  chmod u+r "$dirname"
}

read -p "Enter dirname to give read permission: " dirname

readPermissionToDir "$dirname"