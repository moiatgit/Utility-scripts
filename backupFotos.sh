#! /bin/bash
# Còpia de seguretat a disc de 500Gb
#
OPCIONS="-vuRpP"     # Opcions de còpia
ORIGEN=/mnt/dades/images
DESTINACIONS="/media/Maxtor500Gb/fotos /media/backup2TB/blami/images /media/backup3TB/fotos /media/Iomega_HDD/fotos"
#
for DEST in $DESTINACIONS
do
    if [ -d $DEST ]
    then
        nice cp $OPCIONS $ORIGEN/* $DEST/
        echo "Últim backup `date`" >> $DEST/historic.backups.txt
    fi
done
#
exit 0
