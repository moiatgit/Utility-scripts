#!/bin/sh
current=`pwd`
echo $current
cd /home/moi/dev/sync_feina
/usr/bin/python ./Skz.py
cd $current
echo -n Còpia de seguretat al Dropbox .. 
cp -pRu /home/moi/Feina/ies_2011_12/* /home/moi/Dropbox/wrk/ies_2011_12/
echo . Realitzada
