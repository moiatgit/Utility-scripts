#! /bin/bash
#
# Synchronization script
#
# It allows synchronization of different git repositories in multiple media.
# It assumes each git repository has a remote named $BARE_REPO_NAME
#
# Configuration file is ~/.SimpleSkz with contents:
#
#   PROJECT_LIST=("path to project1","path to project2")
#
# For each project in PROJECT_LIST:
#   - enter in the folder
#   - checks whether the path corresponds to a git repository
#   - pulls everything fom $BARE_REPO_NAME
#   - adds **any** change in the project allowed by .gitignore
#   - commits all changes
#   - pushes everything to $BARE_REPO_NAME
# In case of any error, it just stops
#
# It defines a default comment for the commits, unless $1 contains something to put there instead.
# 
# TODO: current version requires including each repository in $PROJECT_LIST although they could be
# dependent (in the remote list of a previous repository) You can do it automatically by reviewing
# each remote not $BARE_REPO_NAME (remember there's the path!)

source ~/.SimpleSkz
BARE_REPO_NAME=repo

# Define comment for commit
if [ -z "$1" ];
then
    COMMIT_COMMENT="`date`"
else
    COMMIT_COMMENT="$1"
fi

TMPFILE="/tmp/Skz_`date`.$RANDOM"

commit () {
    # commits on cwd
    # it recursively adds all the possible changes to the repository
    echo -n "... Committing: "
    find . -type d | grep -v "\.\w" | sed "s/\(.*\)/\"\1\"/g" | xargs git add -A &> "$TMPFILE"
    if [ `LANG=en_US.UTF-8 git status | grep "nothing to commit" | wc -l` -eq 1 ];
    then
        echo "no changes"
    else
        echo
        git commit -am "$COMMIT_COMMENT"
        changes_commited=1
    fi
}

gitpull () {
    # pulls from $BARE_REPO_NAME
    echo -n "··· Pulling from $BARE_REPO_NAME: "
    git pull "$BARE_REPO_NAME" master &> "$TMPFILE"
    if [[ ! -n $(grep "Already up-to-date." "$TMPFILE") ]];
    then
        echo
        cat "$TMPFILE"
    else
        echo "no changes"
    fi
}

gitpush () {
    # pushes to $BARE_REPO_NAME
    echo -n "··· Pushing to $BARE_REPO_NAME: "
    git push "$BARE_REPO_NAME" master &> "$TMPFILE"
    if [[ ! -n $(grep "Everything up-to-date" "$TMPFILE") ]];
    then
        echo
        cat "$TMPFILE"
    else
        echo "no changes"
    fi
}
#
num_repos=${#PROJECT_LIST[@]}
r=0
while [ "$r" -lt "$num_repos" ];
do
    current_repository=${PROJECT_LIST[$r]}

    # Check if the folder exists
    if [ ! -d $current_repository ];
    then
        echo "ERROR: review if $current_repository does really exist"
        exit 1
    fi

    cd $current_repository

    # check if the folder is a git repository
    if [ `git status 2>&1 |  grep "^fatal:" | wc -l` -eq 1 ]; 
    then
        echo "ERROR: review if $current_repository is a git repository"
        exit 1
    fi

    # check if the repository does have a $BARE_REPO_NAME remote
    if [ `git remote | grep "^$BARE_REPO_NAME\$" | wc -l` -eq 0 ];
    then
        echo "ERROR: review if $current_repository repository has a remote named repo"
        exit 1
    fi

    echo "Processing repository $current_repository"

    # pull from $BARE_REPO_NAME
    gitpull $BARE_REPO_NAME

    # commiting everything in this repository
    changes_commited=0
    commit

    # pushing changes to $BARE_REPO_NAME
    if [ $changes_commited -eq 1 ];
    then
        gitpush $BARE_REPO_NAME
    fi

    let "r++"
done


