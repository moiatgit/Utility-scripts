#! /bin/sh
# Sincronitza ies-continguts
# Espera a ~/.sincro.ies-continguts la definició de $repositories i $branches

# TODO: es pot generalitzar a la resta de repositoris ara que les branques són obtingudes dels
# diferents repositoris git directament.

sincroniza(){
    echo "Sincronització de continguts amb $1"
    if [ ! -d "$1" ];
    then
        echo "No està accessible $1"
    else
        cd "$1"
        for branch in $branches;
        do
            echo "Syncing on $branch"
            git checkout $branch
            bash gitpull.sh
            bash gitpush.sh
        done
    fi
}


. $HOME/.sincro.ies-continguts

if [ -z "$repositories" ];
then
    echo "Problema amb la definició dels repositoris"
    echo "Assegurat que ~/.sincro.ies-continguts és correcte"
    exit 1
fi


cd "$local"

if [ -z "`LANG=en git status | grep 'nothing to commit'`" ];
then
    echo "El repositori actual no està net. Revisa-ho abans de continuar"
    exit 1
fi


startbranch=`LANG=en git status | grep "On branch" | cut -d " " -f 3`
for p in $repositories;
do
    sincroniza $p
done
git checkout $startbranch
