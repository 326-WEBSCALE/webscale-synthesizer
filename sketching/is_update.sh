#!bin/bash
# Script to print contents of a file whenever the file is
# modified. Useful when working with programs that send
# their outputs to a file

set -eu

FIND_ARGS=". -maxdepth 1 -name $1 -mtime -2s"

while [ 1 ]; do
  FILE_NAME=`find $FIND_ARGS`
  if [ "$FILE_NAME" != "" ]; then
    clear
    echo "----- " $FILE_NAME " ------"
    cat $FILE_NAME
    sleep 1
  fi
done
