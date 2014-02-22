#! /bin/bash

echo "Use this script to launch the mongod server"
echo "press enter to continue <ctrl>-c to cancel"
read resposta

a="$(pidof mongod)"
if [ "$a" == "" ]
then
    mongod --dbpath ~/Estudi/mongodb/data/ &
else
    echo "Already running with pid $a"
fi

