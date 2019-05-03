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

# TODO: small improvement: allow args specifying the repo so this script cd on
# this repo.

# TODO: current version presents the following problem when the repo has more
# than one remote. It pull-pushes the contents of each repo in the order given
# by ``git remote`` so it is possible that the contents of the repo changes with
# the second sync but the first remote won't know them until a new execution is
# performed.
# It could be soved by first pulling from all the remotes and then pushing

# TODO: current version has a problem: when there's a warning on branch
# change (e.g. there're some files in a non registered folder that can be
# removed) the branch simply gets unsynced


error() { echo "ERROR: $1" >&2; exit 1; }

# check commandline arguments
commit_first=0      # add all changes and commit first

for option in "$@"
do
    case "$option" in

        "-h") echo "Usage: $0 [-h | [-c [comment]]]"
              echo "-h: displays this help and exits"
              echo "-c: add any change in current branch and commits with comment"
              exit 0
            ;;

        "-c") commit_first=1
              commit_comment="`date`"
            ;;

        *) if [ "$commit_first" -eq 1 ];
           then
               commit_comment="$option"
           else
               error "Invalid option $option. Use -h for help"
           fi
    esac
done

# Is $PDW a git repository?
LANG=en_US.UTF-8 git status &> /dev/null || error "Not a git repository"

# Is this repo dirty? (there are uncommited changes?)
if [ "$commit_first" -eq 1 ];
then
    git add --all
    git commit -am "$commit_comment"
else
    [[ "`LANG=en_US.UTF-8 git status | grep -c 'Changes'`" == 0 ]] || error "Changes not staged for commit"
fi


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
