#! /bin/sh
echo "sudo apt-get update"
sudo apt-get update
if [ "$?" ];
then
    echo "c to upgrade, anything else otherwise"
    read resp
    if [ "$resp" = "c" ];
    then
        echo "sudo apt-get upgrade"
        sudo apt-get upgrade
    else
        echo "Not upgraded"
    fi
else
    echo "Error/s found"
fi
