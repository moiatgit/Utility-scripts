#! /bin/sh
# Sincronitza ies-continguts
# Espera a ~/.sincro.ies-continguts la definició de $repositories

# TODO: es pot generalitzar a la resta de repositoris si fas que les branques siguin obtingudes dels
# diferents repositoris git directament.

sincroniza(){
    echo "Sincronització de continguts amb $1"
    if [ ! -d "$1" ];
    then
        echo "No està accessible $1"
    else
        cd "$1"
        for branch in master online oldstuff dev-cursxml;
        do
            git checkout $branch
            bash gitpull.sh
            bash gitpush.sh
        done
        git checkout master
    fi
}


. $HOME/.sincro.ies-continguts

if [ -z "$repositories" ];
then
    echo "Problema amb la definició dels repositoris"
    echo "Assegurat que ~/.sincro.ies-continguts és correcte"
    exit 1
fi

for p in $repositories;
do
    sincroniza $p
done
