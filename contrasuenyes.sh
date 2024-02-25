#! /bin/sh
vimflavor=vim
filetoopen=$HOME/.config/contrasuenyes/.contrasuenyes

TERMINAL=gnome-terminal     # xfce4-terminal

version5=$(LANG=en bash --version | grep "GNU bash, version 5")
if [ -z "$version5" ];
then
    $TERMINAL -e "$vimflavor -p \"$filetoopen\""
else
    OPTION="-q"
    $TERMINAL $OPTION -- $vimflavor -p "$filetoopen"
fi
