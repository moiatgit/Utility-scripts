#! /bin/bash
#

folder=${1:-.}  # arg 1 or . if unset or empty string
echo "This script will remove all the broken symlinks at $folder"
find -L $folder -type l
echo "press enter to continue <ctrl>-c to cancel"
read resposta

find -L $folder -type l -exec rm -v {} +
