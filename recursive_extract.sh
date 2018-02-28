#! /bin/bash
# This script decompreses packages from current folder
# It considers the mime-type of the file to decide the alrogithm
#
# Original packages are left there so, subsequent executions of this script will lead the
# user to deal with the overwritting politics of each uncompressing utility
#
# TODO: add capability to extract again in case $rename_option=1 and once
# extracted, a package contained further packages! It could be performed
# by iterative execution (i.e. a loop) and a counter of the number of
# packages extracted in each iteration, until the counter gets 0
#
interactive_option=1    # the script is running interactively. i.e. It will prompt the user
                        # When not in interactive mode, it won't prompt and rename option will be set
rename_option=0

extract() {
    # checks whether the folder $1 already exists. If not, it creates it
    # and extracts $3 file with $2 command inside the new folder
    newdir=$1
    command=$2
    src=$3
    if [ -d "$newdir" ];
    then
        echo "Folder `pwd`/$newdir already exists: no action"
    else
        mkdir -p "$newdir"
        cd "$newdir"
        eval $command \"$src\"
        if [[ "$rename_option" == 1 ]];
        then
            mv "$src" "$src.decompressed"
        fi
    fi
}

processa() {
    path=$(dirname $1)
    name=$(basename $1)

    mimetype=`file --mime-type "$1" | rev | cut -d ':' -f 1 | rev | tr -d [:space:]`

    extension="${name##*.}"
    src="../$name"
    basedir="$PWD"
    newdir="$name.files"

    cd "$path"
    command=""
    if [[ "$mimetype" == "application/java-archive" ]]
    then
        command="jar xvf"
    elif [[ "$mimetype" == "application/x-bzip2" ]]
    then
        command="tar xjvf"
    elif [[ "$mimetype" == "application/gzip" ]]
    then
        command="tar xzvf"
    elif [[ "$mimetype" == "application/x-tar" ]]
    then
        command="tar xvf"
    elif [[ "$mimetype" == "application/x-xz" ]]
    then
        command="tar xJvf"
    elif [[ "$mimetype" == "application/zip" ]]
    then
        command="jar xvf"
    elif [[ "$mimetype" == "application/x-rar" ]]
    then
        command="unrar x"
    elif [[ "$mimetype" == "application/x-7z-compressed" ]]
    then
        command="7za e"
    fi
    if [[ -n $command ]];
    then
        extract $newdir $command $src
    fi

    cd "$basedir"
}

if [[ "$1" == "-I" ]];
then
    interactive_option=1
    rename_option=1
else 
    echo "This script will decompress any package from current folder"
    if [[ "$1" == "-r" ]];
    then
        rename_option=1
    else
        echo "Running with option -r, it will rename the original packages with the suffix .decompressed"
    fi
    echo "press enter to continue <ctrl>-c to cancel"
    read resposta
fi

SAVEIFS=$IFS
IFS=$(echo -en "\n\b")
files=`find . -type f`
for f in $files;
do
    if [[ "${f##*.}" != "decompressed" ]];
    then
        processa "$f"
    fi
done
IFS=$SAVEIFS

