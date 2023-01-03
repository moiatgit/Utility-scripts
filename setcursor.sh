#! /bin/bash
if [ "$1" == "gran" ];
then
    gsettings set org.gnome.desktop.interface cursor-size 48
else
    gsettings set org.gnome.desktop.interface cursor-size 24
fi
