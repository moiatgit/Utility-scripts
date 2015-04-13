#! /bin/bash
echo "Launch PostGreSQL server (virtualmachine)"
VBoxManage startvm "Ubuntu PostGreSQL"
if [ "$?" == 0 ];
then
    echo "Done. PostGreSQL server is now accessible at 192.168.56.101"
else
    echo "ERROR: problem trying to launch PostGreSQL server"
fi
