#! /bin/bash
ping -c 1 blamihost.blami.net &> /dev/null
if [[ "$?" == "0" ]];
then
    scp -p moi@blamihost.blami.net:.contrasuenyes $HOME/
else
    echo "out"
fi
