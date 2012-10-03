#! /bin/bash

# Allows folder contents comparison
# It computes md5sum for every file in both folders and
# put results on two /tmp files. Finally it executes diff to
# check differences
#
if [ "$#" -ne "2" ]
then
    echo "Usage: $0 dir1 dir2"
    exit 1
fi
if [ -d "$1" -a -d "$2" ]
then 
    find $1 -type f -exec md5sum {} \; | cat > /tmp/0000000000000_.txt 
    find $2 -type f -exec md5sum {} \; | cat > /tmp/1111111111111_.txt
    cut -f 1 -d " " /tmp/0000000000000_.txt  | sort > /tmp/0000000000000.txt 
    cut -f 1 -d " " /tmp/1111111111111_.txt  | sort > /tmp/1111111111111.txt 
    diff /tmp/0000000000000.txt /tmp/1111111111111.txt
fi
echo "ok"
