#! /bin/bash
# Còpies de seguretat del directori /home/moi
#

OPCIONS="-rpEogtu"                  # Opcions de còpia
DESTINACIO=("/media/backup2TB" "/media/backup3TB")    # On es guardarà la còpia
USUARI="moi"                        # subcarpeta dins de destinació
FITXER_LOG="backupmoi.log"          # Nom del fitxer de log
EXCLUSIONS='--exclude=.git --exclude=.skz --exclude=*~' # elements a excloure
CARPETES=("/mnt/dades/home/moi/Feina" "/mnt/dades/dev" "/mnt/dades/Libros" "/mnt/dades/Musica"  "/mnt/dades/home/moi/Estudi" "/mnt/dades/home/moi/Documents")
#
# Neteja de fitxers temporals
/home/moi/bin/neteja.sh
#
for dest in ${DESTINACIO[*]};
do
    if [ -d "$dest" ];
    then
        echo "backup $dest"
        for carpeta in ${CARPETES[*]};
        do
            nomcarpeta=$(basename $carpeta)     # nom de la carpeta on deixar
            finaldest="$dest/$nomcarpeta"       # destinació final de la còpia
            echo "Backup de $carpeta a $finaldest"
            mkdir -p "$finaldest"
            echo "`date` - inici backup" >> "$finaldest/$FITXER_LOG"
            rsync $OPCIONS $EXCLUSIONS "$carpeta/" "$finaldest"
            echo "`date` - final backup" >> "$finaldest/$FITXER_LOG"
        done
    fi
done
