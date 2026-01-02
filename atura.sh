#! /bin/bash
# This script requires that '$ sudo pm-suspend' doesn't require
# password.
# If you can afford the risk in your system, you can simply add the
# following line to visudo
#
#   «yourusername» ALL=(root) NOPASSWD: /usr/sbin/pm-suspend




echo -n "Suspending the system "
if [[ -z "$1" ]];
then
    echo "now"
    sudo systemctl suspend -i
else
    echo "in $1"
    sleep "$1" && sudo systemctl suspend -i
fi

