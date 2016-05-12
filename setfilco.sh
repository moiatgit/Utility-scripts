#! /bin/sh
# reset current layout with a general one
echo "Key remaping for Filco 91"
setxkbmap -layout es -model 105
#switch_keyboard_filco.sh
#set_Xmodmap_for_filco91.sh goca
xmodmap Xmodmap.ca.filco91
