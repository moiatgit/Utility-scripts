#! /bin/bash
#
# Moves $1(f) to $2 and creates a softlink on $1 to $2/f
#
if [ -z "$1" -o -z "$2" ];
then
    echo "Usage: $0 source_path destination_path"
    exit 1
fi

if [ ! -f "$1" -o -h "$1" ];
then
    echo "ERROR: $1 not a regular file"
    exit 2
fi

if [ ! -d "$2" ];
then
    echo "ERROR: $2 not a directory"
    exit 3
fi

sfname=$(basename $1)
dfpath=${2%/}/$sfname

if [ -f $dfpath ];
then
    echo "ERROR: $dfpath already exists"
    exit 4
fi

echo "Operations to perform:"
echo "$ mv $1 $dfpath"
echo "$ ln -s $dfpath $1"
read -p "Proceed? [Yn] " -n 1 -r
if [[ $REPLY =~ ^[YySs]$ ]]
then
    mv "$1" "$dfpath"
    ln -s "$dfpath" "$1"
    echo
    if [ $? -eq 0 ];
    then
        echo "done"
    fi
else
    echo
    echo "No change"
fi
