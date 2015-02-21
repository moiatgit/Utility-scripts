#! /bin/bash

echo "Use this script to remove all old kernels in this system"
echo "press a key to continue <ctrl>-c to cancel"
read resposta

sudo apt-get remove --purge $(dpkg -l 'linux-*' | sed '/^ii/!d;/'"$(uname -r | sed "s/\(.*\)-\([^0-9]\+\)/\1/")"'/d;s/^[^ ]* [^ ]* \([^ ]*\).*/\1/;/[0-9]/!d')
