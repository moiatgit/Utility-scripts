#! /bin/bash
#
# Synchronization script
#
# tries to synchronize local repository with its pen's counterpart
# It accepts one or more pendrives
#
# ~/.Skz should contain configuration in the following format:
#    LOCAL="«path to local rep"
#    PEN=("«path to one pendrive»" "«path to another pendrive»")
#    LOCAL_NAME=«host name rep»
#    PEN_NAME=("«pen1 name rep»" "«pen2 name rep»")
#
# TODO: add robustness
#       add option to prepare a repositori from given path and add it to
#       everywhere it should be: .Skz, remotes...
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

    num_pen=${#PEN[@]}
    num_pen_name=${#PEN_NAME[@]}
    if [ "$num_pen" -ne "$num_pen_name" ];
    then
        echo "ERROR: PEN and PEN_NAME length's must match"
        exit 1
    fi
    #
    i=0
    while [ "$i" -lt "$num_pen" ];
    do
        pen_path=${PEN[$i]}
        if [ -d "$pen_path" ];
        then
            rep_name=${PEN_NAME[$i]}
            commit $pen_path
            cd $LOCAL
            echo "··· Pulling from $pen_path"
            git pull $rep_name master
            cd $pen_path
            echo "··· Pulling from $LOCAL"
            git pull $LOCAL_NAME master
        fi
        let "i++"
    done
fi

