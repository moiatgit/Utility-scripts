#! /bin/bash
echo "Connecting to the mgome virtual machine"
cd $ies/vm/debian12/
vagrant status | grep 'not running' && vagrant up
vagrant ssh
