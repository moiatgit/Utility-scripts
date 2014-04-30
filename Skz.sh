#! /bin/bash
#
# Synchronization script
#
# tries to synchronize local repository with its pen's counterpart
# It adds also the possiblity to just backup (JBK) without expecting
# changes in destination repository
#
# It accepts one or more pendrives and jbk
# It accepts one or more repositories. By now all them must be stored
# at the same base dir.
#
# ~/.Skz should contain configuration in the following format:
#    LOCAL_BASE="«path to local base of repositories"
#    PEN_BASE=("«path to one pendrive's base»" "«path to another pendrive's #    base»")
#    LOCAL_NAME=«host name rep»
#    PEN_NAME=("«pen1 name rep»" "«pen2 name rep»")
#    REPOS=("«path to repo1»" "«path to repo 2»")
# When pen name repository starts with -- Skz treats as JBK and no commit is
# performed on this repository.
#
# TODO: add robustness and config flexibility
#
source ~/.Skz

#
if [ -z "$1" ];
then
    COMMIT_COMMENT="`date`"
else
    COMMIT_COMMENT="$1"
fi

TMPFILE="/tmp/`date`.$RANDOM"
#
commit () {
    # commits on path $1 if exists
    # it recursively adds all the possible changes to the repository
    if [ -d $1 ];
    then
        cd $1
        find . -type d | grep -v "\.\w" | sed "s/\(.*\)/\"\1\"/g" | xargs git add -A

        if [[ ! -n $(git commit -am "$COMMIT_COMMENT" | tee "$TMPFILE" | grep "nothing to commit (working directory clean)") ]];
        then
            echo "··· Commit on $1"
            cat "$TMPFILE"
        else
            echo "... Commit on $1: no changes"
        fi
    fi
}

pull () {
    # pulls from $1 directory with name $2 to $3
    cd "$1"
    if [[ ! -n $(git pull "$2" master | tee "$TMPFILE" | grep "Already up-to-date.") ]];
    then
        echo "··· Pulling from $2 to $3"
        cat "$TMPFILE"
    else
        echo "... Pulling from $2 to $3: no changes"
    fi
}
#
num_repos=${#REPOS[@]}
r=0
while [ "$r" -lt "$num_repos" ];
do
    repo=${REPOS[$r]}
    LOCAL="$LOCAL_BASE/$repo"
    #
    if [ -d $LOCAL ];
    then
        echo "Syncing repository $repo"
        commit $LOCAL
        num_pen=${#PEN_BASE[@]}
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
            pen_path="${PEN_BASE[$i]}/$repo"
            if [ -d "$pen_path" ];
            then
                rep_name=${PEN_NAME[$i]}
                if [[ $rep_name == "--"* ]]; # check whether it is a just backup rep (JBR)
                then
                    rep_name=${rep_name:2}  # extract -- from repository name
                else
                    commit $pen_path
                    pull "$LOCAL" "$rep_name" "$LOCAL_NAME"
                    #cd $LOCAL
                    #echo "··· Pulling from $rep_name to $LOCAL_NAME"
                    #git pull $rep_name master
                fi
                pull "$pen_path" "$LOCAL_NAME" "$rep_name"
                #cd $pen_path
                #echo "··· Pulling from $LOCAL_NAME to $rep_name"
                #git pull $LOCAL_NAME master
            fi
            let "i++"
        done
    fi
    let "r++"
done
