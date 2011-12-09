#! /bin/bash
#
# Intenta compilar tots els *.java que troba 
# en els subdirectoris a partir del cwd
#
echo "Es compilaran tots els fitxers .java que es trobin a partir del directori actual"
echo "Prem c + <ENTER> per continuar"
read resposta
if [ "$resposta" == "c" ]
then
    oldIFS=$IFS
    IFS=$'\n'       # change field separator
    fitxers=`find . -name *.java -type f`
    for f in $fitxers
    do
        nomdir=`dirname "$f"`
        nomfit=`basename "$f"`
        cd "$nomdir"
        `javac $nomfit &> /dev/null`
        if [ $? -ne 0 ];
        then
            echo "$f ko";
        fi
        cd -
    done
    IFS=$oldIFS
else
    echo "No s'ha realitzat cap canvi"
fi
