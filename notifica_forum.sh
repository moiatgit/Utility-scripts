#! /bin/bash
# This script shows the result of checking for forum entries.
# and if there're any unread entries it shows it as a notification.
# It uses notify-send utility from libnotify-bin package
#
# Put a call to this script at the startup application list if you
# want to get notifications when login
#
# TODO: replace the need of temporary file (load response on memory)
#
fitxer=/tmp/ies_checkforums.py.resposta
~/bin/ies_checkforums.py > $fitxer
if [[ -s $fitxer ]]
then
    /usr/bin/notify-send "`cat $fitxer`"
fi
