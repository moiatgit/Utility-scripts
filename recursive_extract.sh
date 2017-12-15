#! /bin/bash
# This script decompreses packages from current folder
# It considers the mime-type of the file to decide the alrogithm
#
# Original packages are left there so, subsequent executions of this script will lead the
# user to deal with the overwritting politics of each uncompressing utility
#

echo "This script will decompress any package from current folder"
echo "press enter to continue <ctrl>-c to cancel"
read resposta

processa() {
    echo "On file $1"
    path=$(dirname $1)
    name=$(basename $1)

    mimetype=`file --mime-type "$1" | rev | cut -d ':' -f 1 | rev | tr -d [:space:]`
    echo "XXX $mimetype"

    extension="${name##*.}"
    src="../$name"
    basedir="$PWD"
    newdir="$name.files"

    cd "$path"
    if [[ "$mimetype" == "application/java-archive" ]]
    then
        mkdir -p "$newdir"
        cd "$newdir"
        jar xvf "$src"
    elif [[ "$mimetype" == "application/x-bzip2" ]]
    then
        mkdir -p "$newdir"
        cd "$newdir"
        tar xjvf "$src"
    elif [[ "$mimetype" == "application/gzip" ]]
    then
        mkdir -p "$newdir"
        cd "$newdir"
        tar xzvf "$src"
    elif [[ "$mimetype" == "application/x-tar" ]]
    then
        mkdir -p "$newdir"
        cd "$newdir"
        tar xvf "$src"
    elif [[ "$mimetype" == "application/x-xz" ]]
    then
        mkdir -p "$newdir"
        cd "$newdir"
        tar xJvf "$src"
    elif [[ "$mimetype" == "application/zip" ]]
    then
        mkdir -p "$newdir"
        cd "$newdir"
        jar xvf "$src"
    elif [[ "$mimetype" == "application/x-rar" ]]
    then
        mkdir -p "$newdir"
        cd "$newdir"
        unrar x "$src"
    elif [[ "$mimetype" == "application/x-7z-compressed" ]]
    then
        mkdir -p "$newdir"
        cd "$newdir"
        7za e "$src"
    fi

    cd "$basedir"
}

SAVEIFS=$IFS
IFS=$(echo -en "\n\b")
#files=`find . -type f \( -name '*.zip' -o -name '*.tar.gz' -o -name '*.jar' \)`
files=`find . -type f`
for f in $files;
do
    processa "$f"
done
IFS=$SAVEIFS

