#! /bin/bash
#
# Synchronization script
#
# Tries to sincronize current git repository for all its branches
# branches to all its remotes

echo "This script is under development"
exit 1

error() { echo "ERROR: $1" >&2; exit 1; }

GITCOMMAND="LANG=en_US.UTF-8 git"

# Is $PDW a git repository?
LANG=en_US.UTF-8 git status &> /dev/null || error "Not a git repository"

# Is this repo dirty? (there are uncommited changes?)

[[ "`LANG=en_US.UTF-8 git status | grep -c 'Changes not staged for commit'`" == 0 ]] || error "Changes not staged for commit"

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
    echo "Remote $remote is available"
done
# for each remote in this repository
#   check if remote contains @ -> a net remote
#       check if net remote is accessible (ping)
#   otherwise -> a mounted remote
#       check if mounted remote is accessible (folder exists)
#   In case a remote is available:
#       fetch all branches
#       push all branches
#

