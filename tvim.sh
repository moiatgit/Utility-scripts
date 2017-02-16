#! /bin/bash
#
# This script opens a new terminal and opens a vim edition on $@

TERMINAL=gnome-terminal
OPTION="-e"


if [ $# -eq 0 ];
then
    $TERMINAL $OPTION "vim $PWD"
fi

VALUES=( "$@" )
CURRENT="$PWD/"
FILES="${VALUES[@]/#/$CURRENT}"
$TERMINAL $OPTION "vim -p $FILES"

