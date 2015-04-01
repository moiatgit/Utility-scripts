#! /bin/bash
#
echo "Switche keyboard layout to/from Filco's Majestouch tenkeyless with JA layout"

if [[ `setxkbmap -query | grep "layout:     jp"` == "" ]]
then
    setxkbmap -layout jp -variant jpcat
    if [ "$?" ]
    then
        echo "Changed to jp layout"
    else
        echo "ERROR"
    fi
else
    echo "Already jp"
    setxkbmap -layout es -variant cat
    if [ "$?" ]
    then
        echo "Restored to es layout"
    else
        echo "ERROR"
    fi
fi

