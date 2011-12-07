#! /bin/bash
#
# Descomprimeix tots els fitxers .tar, .tar.gz, .rar, .zip que troba 
# en els subdirectoris a partir del cwd
#
echo "Es descomprimiran tots els fitxers a partir del directori actual"
echo "Prem c + <ENTER> per continuar"
read resposta
if [ "$resposta" == "c" ]
then
    oldIFS=$IFS
    IFS=$'\n'       # change field separator
    fitxers=`find . -type f`
    for f in $fitxers
    do
        nomdir=`dirname "$f"`
        nomfit=`basename "$f"`
        extfit="${nomfit##*.}"
        cd "$nomdir"
        if [ "$extfit" == "rar" ]
        then
            unrar e "$nomfit"
        elif [ "$extfit" == "zip" ]
        then
            unzip "$nomfit"
        elif [ "$extfit" == "gz" ]
        then
            tar -xvzf "$nomfit"
        elif [ "$extfit" == "tar" ]
        then
            tar -xvf "$nomfit"
        fi
        cd -
    done
    IFS=$oldIFS
else
    echo "No s'ha realitzat cap canvi"
fi
