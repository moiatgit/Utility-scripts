#! /bin/sh
echo "Launches Android Development Tools with Eclipse"
a="$(pidof eclipse)"
if [ "$a" != "" ]
then
    echo "Eclipse already running with pid $a"
    echo "press a key to continue <ctrl>-c to cancel"
    read resposta
fi

~/soft/adt-bundle-linux-x86_64-20131030/eclipse/eclipse &

