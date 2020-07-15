#! /bin/bash

# Syncs the $ies_continguts repository
# It requires $ies_continguts to be set to an existing folder

error() { echo "ERROR: $1" >&2; exit 1; }

if [ -z "$ies_continguts" ];
then
    error "Var \$ies_continguts not defined"
fi

if [ ! -d "$ies_continguts" ];
then
    errot "Var \$ies_continguts is pointing to a non directory $ies_continguts"
fi
cd "$ies_continguts"

LANG=en_US.UTF-8 git status &> /dev/null || error "Not a git repository"

NewSkz.sh
