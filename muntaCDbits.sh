#! /bin/sh
echo $1
sudo mount -t iso9660 -o loop "$1" /media/cdrom/
