#! /bin/bash
# Còpies de seguretat
#
OPCIONS="-vuRpP"                    # Opcions de còpia
DESTINACIO=("/media/backup2TB/" "/media/backup3TB/")    # On es guardarà la còpia
FITXER_LOG="backup2TB.log"          # Nom del fitxer de log
#
/home/moi/bin/neteja.sh
#
echo Recorda que caldrà que revisis la còpia de seguretat de blami quan hi hagi massa espai ocupat a Seagate2Tb
#
for USUARI in moi   # sil
do
    echo "Backup de l'usuari $USUARI"
    sudo echo "`date` - inici backup" >> $DESTINACIO/$USUARI/$FITXER_LOG
    sudo cp $OPCIONS /home/$USUARI/ $DESTINACIO
    sudo echo "`date` - final backup" >> $DESTINACIO/$USUARI/$FITXER_LOG
done
