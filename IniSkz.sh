#! /bin/bash
#
# Preparation of repositories for the Skz script
#
# Checks whether the repositories implied in ~/.Skz do exit as
# repositories. Otherwise it creates them.
#
# ~/.Skz should contain the same information as expected by Skz.sh
# script
#
source ~/.Skz
#
# The following function initializes a repository with git and the
# required remotes
initialize() {
    if [ ! -d "$1" ];
    then
        echo "Creating folder $1"
        mkdir -p "$1"
    fi
    if [ ! -d "$1/.git" ];
    then
        echo "Creating repository $1"
        cd "$1"
        git init
        echo "This repo has been automaticaly created by $0" > README
        git add README
        git commit -am "First commit: automated by $0"

    fi
}

# the following function adds a remote $2 to a repository $1 with name $3
add_remote() {
    cd $1
    if [[ ! -n $(git remote -v | cut -f 1 | grep "$3") ]];
    then
        echo "Adding remote $2 to $1 with name $3"
        git remote add $3 "$2"
    fi
}
#
num_pen=${#PEN_BASE[@]}
num_repos=${#REPOS[@]}
r=0
while [ "$r" -lt "$num_repos" ];
do
    repo=${REPOS[$r]}
    LOCAL="$LOCAL_BASE/$repo"
    #
    if [ -d "$LOCAL_BASE" -a ! -d "$LOCAL/.git" ];
    then
        initialize $LOCAL
    fi
    #
    i=0
    while [ "$i" -lt "$num_pen" ];
    do
        pen_path="${PEN_BASE[$i]}/$repo"
        if [ -d ${PEN_BASE[$i]} ];
        then
            if [ ! -d "$pen_path/.git" ];
            then
                initialize $pen_path
            fi
            add_remote $pen_path $LOCAL $LOCAL_NAME
            add_remote $LOCAL $pen_path ${PEN_NAME[$i]}
        fi
        let "i++"
    done
    let "r++"
done
