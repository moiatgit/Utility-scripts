#! /bin/bash
#
# Synchronization script
#
# tries to synchronize local repository with its pen's counterpart
#
LOCAL="/home/moi/Feina/ies_2012_13"
PEN="/media/moises_pen8gb/ies_2012_13"
#
commit () {
    # commits on path $1 if exists
    # it recursively adds all the possible changes to the repository
    if [ -d $1 ];
    then
        echo "··· Commit on $1"
        cd $1
        find . -type d | grep -v "\.\w" | sed "s/\(.*\)/\"\1\"/g" | xargs git add -A
        git commit -am "`date`"
    fi
}
#
if [ -d $LOCAL ];
then
    commit $LOCAL
    if [ -d $PEN ];
    then
        cd $LOCAL
        echo "··· Pulling from $PEN"
        git pull pen master
        commit $PEN
        cd $PEN
        echo "··· Pulling from $LOCAL"
        git pull host master
    fi
fi

