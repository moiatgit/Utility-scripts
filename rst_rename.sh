#! /bin/bash

# This script renames rst files in args while replacing references
# in any file placed in any folder from pwd

# TODO: it should be improved the selection of the common folder.
# Currently it allows running it over a file that is not in the path
# of the possible referencers

# check if there're the two required args
if [ "$#" -ne 2 ];
then
    echo "Usage: $0 «path to filename» «destination filename»"
    exit 1
fi

ext="${1##*.}"

# check if the file has a proper extension
if [[ $ext == $1 ]];
then
    echo "WARNING: sorry, this version just works for files with extension"
    exit 1
fi

# check if destination file has path information
if [ $(basename "$2") != "$2" ];
then
    echo "ERROR: destination filename should not contain any path $2"
    exit 1
fi

# check if file do exits
if [ ! -e "$1" ];
then
    echo "ERROR: file not found $1"
    exit 2
fi

# compose destination file extension if not already present
if [[ ${2##*.} != "$ext" ]];
then
    destfilename="$2.$ext"
else
    destfilename="$2"
fi

# compose destination path
filefolder=$(dirname $1)
destfilepath="$filefolder/$destfilename"

# check if destination file already exists
if [ -e "$destfilepath" ];
then
    echo "ERROR: destination file already exits ($destfilepath). Remove it and rerun $0"
    exit 3
fi

# check whether there're files affected by the renaming
filename=$(basename "$1")

# require confirmation
echo "The following will be performed:"
echo "  $ mv $1 $destfilename"

# check if there are references to the original filename
if [[ "" != $(find . -name '*.rst' -exec egrep -H "\<$filename\>" {} \;) ]];
then
    echo "  The following references to $filename will be replaced by $destfilename"
    find . -name '*.rst' -exec egrep -H "\<$filename\>" {} \;
    references_found=0
else
    references_found=1
fi

read -p "Press c to perform changes, any other key to refrain: " resp
if [[ $resp != "c" ]];
then
    echo "No changes performed. Ease yourself."
    exit 0
fi

# perform changes
if [ $references_found -eq 0 ];
then
    find . -name '*.rst' -exec sed -i "s/\<$filename\>/$destfilename/g" {} \;
fi
mv $1 $destfilepath

echo "Done"
