# Function definitions for the xcd command
# The xcd command allows you to directly jump to a directory when it has been
# marked. Otherwise it will behave as usual cd command

# This file should be sourced by .bashrc or the like. For example, add the
# following line to your ~/.bashrc  (without # of course)
# . ~/bin/xcddef

# Usage:
#   $ xcd name[tab] #  cd to name (with completion) if name is marked, then
#                   #+ goes there, otherwise works as regular cd
#   $ xcd_ls        #  shows list of marked dirs
#   $ xcd_mark      #  marks cwd if not yet
#   $ xcd_unmark    #  unmarks cwd if already marked

export XCD_PATH=$HOME/.config/xcdpaths

function xcd () {

    cd -P $XCD_PATH/$1 &> /dev/null ||  cd $1;
}

function xcd_ls () {
    ls -A $XCD_PATH
}

function xcd_mark () {
    name=$(basename "$PWD")
    if [ -d "$XCD_PATH/$name" ];
    then
        echo "$name already marked"
    else
        ln -s "$PWD" "$XCD_PATH/$name"
    fi
}
function xcd_unmark () {
    name=$(basename "$PWD")
    if [ -d "$XCD_PATH/$name" ];
    then
        rm "$XCD_PATH/$name"
    else
        echo "$name not marked"
    fi
}

function _xcd()
{
    local cur prev opts base
    local names=$( ls -1 $XCD_PATH/ $PWD/ | grep ^$2 | sed '/:$/d' | sed '/^$/d' | sort -u )
    COMPREPLY=( $(compgen -W "${names}") )

}
#complete -o default -o nospace -F _xcd  xcd
complete -o nospace -F _xcd xcd

