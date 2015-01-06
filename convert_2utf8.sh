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
    doconvert="no"
    nomdir=`dirname "$f"`
    nomfit=`basename "$f"`
    cd "$nomdir" &> /dev/null
    file --mime-encoding "$nomfit" | cut --delimiter " " -f 2 > "/tmp/$nomfit.encoding"
    encoding=`cat /tmp/$nomfit.encoding`
    if [[ "$encoding" != "utf-8" ]]
    then
        if [ "`iconv -l | grep -i $encoding`" == "" ]
        then
            echo "No es coneix $encoding per $nomfit"
            doconvert="no"
        else
            iconv -f "$encoding" -t utf-8 "$nomfit" > "/tmp/$nomfit.tmp"
            diff "$nomfit" "/tmp/$nomfit.tmp" > "/tmp/$nomfit.diff"
            if [[ -s "/tmp/$nomfit.diff" ]]
            then
                if [ $force == "no" ]
                then
                    echo "Es convertirà $nomfit de $encoding a utf-8"
                    echo "c per convertir, a per convertir tots, s per saltar aquest, x per finalitzar"
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
                    fi
                else
                    doconvert="yes"
                fi
            fi
        fi
        if [ $doconvert == "yes" ]
        then
            mv "/tmp/$nomfit.tmp" "$nomfit"
            echo "Convertit $nomfit de $encoding a utf-8"
        fi
    fi
cd - &> /dev/null
done
IFS=$oldIFS

