#! /bin/sh
# Sincronitza els repositoris indicats a $repositoris
# Espera a ~/.sincro.repositoris la definició de $repositories

# TODO: add a way to define the remote. Now it is fixed to repo
# TODO: add a way to define the branch. Now it is fixed to master


get_current_branch() {
    tmp=`git symbolic-ref -q HEAD`
    echo ${tmp##refs/heads/}
}

sincroniza(){
    echo "Sincronització de continguts amb $1 pel repositori $2 a la branca $3"
    if [ ! -d "$1" ];
    then
        echo "No està accessible $1"
    else
        cd "$1"
        oldbranch=`get_current_branch`
        git checkout $3
        git pull $2 $3
        git push $2 $3
        git checkout $oldbranch
    fi
}

. $HOME/.sincro.repositoris

if [ -z "$repositories" ];
then
    echo "Problema amb la definició dels repositoris"
    echo "Assegurat que ~/.sincro.ies-continguts és correcte"
    exit 1
fi

for p in $repositories;
do
    sincroniza $p repo master
done


