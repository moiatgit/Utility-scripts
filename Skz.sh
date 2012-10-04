#! /bin/bash
#
# Synchronization script
#
# tries to synchronize local repository with its pen's counterpart
#
source ~/.Skz
#
if [ -z "$1" ];
then
    COMMIT_COMMENT="`date`"
else
    COMMIT_COMMENT="$1"
fi

echo $COMMIT_COMMENT
#
commit () {
    # commits on path $1 if exists
    # it recursively adds all the possible changes to the repository
    if [ -d $1 ];
    then
        echo "··· Commit on $1"
        cd $1
        find . -type d | grep -v "\.\w" | sed "s/\(.*\)/\"\1\"/g" | xargs git add -A
        git commit -am "$COMMIT_COMMENT"
    fi
}
#
if [ -d $LOCAL ];
then
    commit $LOCAL
    if [ -d $PEN ];
    then
        commit $PEN
        cd $LOCAL
        echo "··· Pulling from $PEN"
        git pull $PEN_NAME master
        cd $PEN
        echo "··· Pulling from $LOCAL"
        git pull $LOCAL_NAME master
    fi
fi

