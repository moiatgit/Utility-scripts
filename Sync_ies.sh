#! /bin/bash

# Syncs the $ies repository
# It requires $ies to be set to an existing folder

# It adds --all and commits with $1 as a comment, if present.

error() { echo "ERROR: $1" >&2; exit 1; }

if [ -z "$ies" ];
then
    error "Var \$ies not defined"
fi

if [ ! -d "$ies" ];
then
    errot "Var \$ies is pointing to a non directory $ies"
fi
cd "$ies"

LANG=en_US.UTF-8 git status &> /dev/null || error "Not a git repository"

if [ -z "$1" ];
then
    COMMIT_COMMENT="`date`"
else
    COMMIT_COMMENT="$1"
fi

git add --all
git commit -am "$COMMIT_COMMENT"
NewSkz.sh
