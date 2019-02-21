#! /bin/bash
echo "Key remapping"
if [[ "$1" == en ]];
then
    echo "Mapping en filco91"
    xmodmap $HOME/bin/Xmodmap.en.filco91
else
    echo "General mapping"
    xmodmap $HOME/.Xmodmap
fi
