#! /bin/bash

# this script eases the maintenance of contents at pelican folder
# It requires ~/.pelican2heroku file to know the corresponding paths

PCCONFIG=~/.pelican2heroku

# exit when no configuration found
if [ ! -f  "$PCCONFIG" ]
then
    echo "ERROR: configuration file not found: $PCCONFIG"
    exit 1
fi

# load configuration vars
source $PCCONFIG

# check for correct parameter number
if [ $# -lt 2 ]
then
    echo "ERROR: specify a command (add/rm) and at least one file"
    exit 1
fi

# discriminate option
if [[ "$1" == "add" ]]
then
    action="ADD"
elif [[ "$1" == "rm" ]]
then
    action="RM"
else
    echo "ERROR: available options add and rm"
    exit 1
fi

for f in "${@:2}";
do
    filename="$(readlink -f $f)"
    if [ ! -f "$filename" ]
    then
        echo "WARNING: not found file $filename"
    else
        base=$(basename $filename)
        extension="${base##*.}"
        name="${base%.*}"
        if [[ "$extension" == "rst" ]]
        then
            dirn=$(basename $(dirname $filename))
        elif [[ (("$extension" == "jpg") || ("$extension" == "png")) || ("$extension" == "gif") ]]
        then
            dirn="images"
        else
            dirn="resources"
        fi
        link="$INPUTDIR/$dirn/$base"
        if [ -f "$link" -a $action = "RM" ]
        then
            echo `rm -vi "$link"`
        elif [ ! -f "$link" -a $action = "ADD" ]
        then
            echo `ln -s "$filename" "$link" && ls "$link"`
        else
            echo "WARNING: cannot $action on $link"
        fi
    fi
done

