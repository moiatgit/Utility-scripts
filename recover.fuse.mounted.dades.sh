#! /bin/bash
echo "This script tries to recover /mnt/dades"
echo "Press c to continue. Anything else to cancel"
read resp
if [ "resp" == "c" ];
then
    sudo umount -l /mnt/dades
    sudo mount /mnt/dades
else
    echo "Nothing done"
fi

