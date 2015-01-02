#! /bin/bash
#
# Converteix tots els fitxers del directori actual en utf-8
#
echo "Recodifica els fitxers que es troben a partir d'aquest directori
a UTF-8"
force="no"
oldIFS=$IFS
IFS=$'\n'       # change field separator
fitxers=`find . -type f`
for f in $fitxers
do
    nomdir=`dirname "$f"`
    nomfit=`basename "$f"`
    cd "$nomdir" &> /dev/null
    file --mime-encoding "$nomfit" | cut --delimiter " " -f 2 > "/tmp/$nomfit.encoding"
    encoding=`cat /tmp/$nomfit.encoding`
    if [[ "$encoding" != "utf-8" && "$encoding" != "binary" && "$encoding" != "ERROR" ]]
    then
        iconv -f "$encoding" -t utf-8 "$nomfit" > "/tmp/$nomfit.tmp"
        diff "$nomfit" "/tmp/$nomfit.tmp" > "/tmp/$nomfit.diff"
        if [[ -s "/tmp/$nomfit.diff" ]]
        then
            if [ $force == "no" ]
            then
                echo "Es convertirà $nomfit de $encoding a utf-8"
                echo "c per convertir, a per convertir tots, x per finalitzar"
                read resposta
                if [ "$resposta" == "x" ]
                then
                    exit
                fi
                if [ "$resposta" == "a" ]
                then
                    force="yes"
                    doconvert="yes"
                elif [ "$resposta" == "c" ]
                then
                    doconvert="yes"
                else
                    doconvert="no"
                fi
            fi
            if [ $doconvert == "yes" ]
            then
                mv "/tmp/$nomfit.tmp" "$nomfit"
                echo "Convertit $nomfit de $encoding a utf-8"
            fi
        fi
    fi
    cd - &> /dev/null
done
IFS=$oldIFS

