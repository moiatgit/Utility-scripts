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
    for f in `find .`
    do
        if [ -f $f ]
        then
            nomdir=`dirname $f`
            nomfit=`basename $f`
            extfit=${nomfit##*.} 
            cd $nomdir
            if [ "$extfit" == "rar" ]
            then
                unrar e "$nomfit"
            elif [ "$extfit" == "zip" ]
            then
                unzip "$nomfit"
            fi
            cd -
        fi 
    done
else
    echo "No s'ha realitzat cap canvi"
fi
