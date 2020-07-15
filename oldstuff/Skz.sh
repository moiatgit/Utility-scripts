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
#    Optionally you can add the following variables on the
#    configuration file in order to allow syncing on a bare repository
#
#    BARE_NAME=«name of the bare repo»
#    BARE_URL=«url of the bare repo»
#
#
# performed on this repository.
#
# TODO: use NewSkz to perform the actual syncing.
#   This script should be reprogrammed so it adds all the changes in the
#   repository and then calls NewSkz.sh to finish the work
#
source ~/.Skz

#
if [ -z "$1" ];
then
    COMMIT_COMMENT="`date`"
else
    COMMIT_COMMENT="$1"
fi

TMPFILE="/tmp/Skz_`date`.$RANDOM"
#
commit () {
    # commits on path $1 with name $2 if exists
    # it recursively adds all the possible changes to the repository
    if [ -d $1 ];
    then
        cd $1
        git add --all
        #find . -type d | grep -v "\.\w" | sed "s/\(.*\)/\"\1\"/g" | xargs git add -A
        git commit -am "$COMMIT_COMMENT" &> "$TMPFILE"
        if [[ ! -n $(grep "nothing to commit (working directory clean)" "$TMPFILE") ]];
        then
            echo "··· Commit on $2"
            cat "$TMPFILE"
        else
            echo "... Commit on $2: no changes"
        fi
    fi
}

gitpull () {
    # pulls from $1 directory with repo name $2 to $3
    cd "$1"
    git pull "$2" master &> "$TMPFILE"
    if [[ ! -n $(grep "Already up-to-date." "$TMPFILE") ]];
    then
        echo "··· Pulling from $2 to $3"
        cat "$TMPFILE"
    else
        echo "... Pulling from $2 to $3: no changes"
    fi
}

gitpush () {
    # pushes from repo $2 to $1 directory with name $3
    cd "$1"
    git push "$2" master &> "$TMPFILE"
    if [[ ! -n $(grep "Everything up-to-date" "$TMPFILE") ]];
    then
        echo "··· Pushing from $3 to $2"
        cat "$TMPFILE"
    else
        echo "... Pushing from $3 to $2: no changes"
    fi
}
#
# Determine if it has to sync with a bare repo
if [ ! -z $BARE_NAME ]
then
    BARE_SYNC=1
fi

if [ ! -z $BARE_URL ] && [ ! -z $BARE_SYNC ]
then
    printf "Checking $BARE_URL for bare $BARE_NAME: "
    ping -w 1 -c 1 $BARE_URL > /dev/null
    if [ ! $? -eq 0 ]
    then
        BARE_SYNC=
        printf "Not present\n"
    else
        printf "Done\n"
    fi
fi
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
        #
        if [ ! -z $BARE_SYNC ]
        then
            gitpull $LOCAL $BARE_NAME $LOCAL_NAME
        fi
        #
        commit $LOCAL $LOCAL_NAME
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
                    commit $pen_path $rep_name
                    gitpull "$LOCAL" "$rep_name" "$LOCAL_NAME"
                fi
                gitpull "$pen_path" "$LOCAL_NAME" "$rep_name"
            fi
            let "i++"
        done
        #
        if [ ! -z $BARE_SYNC ]
        then
            gitpush $LOCAL $BARE_NAME $LOCAL_NAME
        fi
    fi
    #
    let "r++"
done

