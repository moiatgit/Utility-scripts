#! /bin/bash
#
# git_pull_all.sh
#
# Pulls all the registered git repositories in the file ~/.config/git_remotes
#  ~/.config/git_remotes is a file that contains lines of the root paths for the
#  local clones of the git repositories.
#  The script will read line by line, cd there if is a folder and performs git pull

config_file=~/.config/git_remotes
# Check confog_file exists
if [ ! -f $config_file ];
then
    echo "ERROR: $config_file not found"
    exit 1
fi

# Read config file
while read -r line;
do
    if [ -d "$line" ];
    then
        echo "Pulling from $line"
        cd "$line"
        git pull
        if [ $? -ne 0 ];
        then
            echo "ERROR: git push failed"
            exit 1
        fi
    else
        echo "ERROR: $line is not a folder"
    fi
done < $config_file
