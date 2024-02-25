#! /bin/bash
ping -c 1 blamihost.blami.net &> /dev/null
if [[ "$?" == "0" ]];
then
    if [[ "$1" == "send" ]];
    then
        scp -p $HOME/.contrasuenyes moi@blamihost.blami.net:.contrasuenyes
    else
        scp -p moi@blamihost.blami.net:.contrasuenyes $HOME/
    fi
else
    echo "out"
fi
