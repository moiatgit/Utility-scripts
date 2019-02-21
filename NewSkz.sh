#! /bin/bash
#
# Synchronization script
#
# Tries to sincronize current git repository for all its branches
# branches to all its remotes

# Place a file .skz_«remotename» in the root directory of a git repository
# for the branches you are interested in syncing for each remote name
# Run this script on the corresponding folder and… you're done
# The script will sync each branch of each remote marked with the
# corresponding file.


error() { echo "ERROR: $1" >&2; exit 1; }

GITCOMMAND="LANG=en_US.UTF-8 git"

# Is $PDW a git repository?
LANG=en_US.UTF-8 git status &> /dev/null || error "Not a git repository"

# Is this repo dirty? (there are uncommited changes?)

[[ "`LANG=en_US.UTF-8 git status | grep -c 'Changes'`" == 0 ]] || error "Changes not staged for commit"

rootfolder=`git rev-parse --show-toplevel`
remotes=`git remote`
for remote in $remotes;
do
    remotehost=`git remote -v | grep $remote | grep '@' | cut -d @ -f 2 | cut -d \  -f 1  | cut -d : -f 1 | sort | uniq`
    if [ -n "$remotehost" ];
    then
        echo "pinging to $remotehost …"
        ping -w 1 -c 1 $remotehost &> /dev/null
        if [ ! $? -eq 0 ]
        then
            echo "$remote on $remotehost is not available"
            continue
        fi
    else
        mountpoint=`git remote -v | grep $remote | cut -d \  -f 1 | cut -f 2 | sort | uniq`
        if [ ! -d $mountpoint ];
        then
            echo "$remote on $mountpoint is not mounted"
            continue
        fi
    fi
    echo; echo "Syncing remote $remote"
    branches=`git for-each-ref --format='%(refname:short)' | grep -v \/`
    startbranch=`LANG=en git status | grep "On branch" | cut -d " " -f 3`
    filemark="$rootfolder/.skz_$remote"
    for branch in $branches;
    do
        git checkout $branch &> /dev/null
        if [ ! -f "$filemark" ];
        then
            echo "Ignoring branch $branch"
            continue
        fi
        echo "Syncing branch $branch"
        git pull $remote $branch || error "Problems pulling repo $repo branch $branch"
        git push $remote $branch || error "Problems pushing repo $repo branch $branch"
    done
    git checkout $startbranch &> /dev/null

done
