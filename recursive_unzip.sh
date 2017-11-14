#! /bin/bash
# This script decompreses packages from current folder
# Original packages are left there so, subsequent executions of this script will lead the
# user to deal with the overwritting politics of each uncompressing utility
#
# XXX TODO: consider using file --mime-type instead of extension to decide the decompressor

echo "This script will decompress any package from current folder"
echo "press enter to continue <ctrl>-c to cancel"
read resposta

processa() {
    echo "On file $1"
    path=$(dirname $1)
    name=$(basename $1)

    extension="${name##*.}"
    src="../$name"
    basedir="$PWD"
    newdir="$name.files"

    cd "$path"
    if [[ "$name" == *.jar ]];
    then
        mkdir -p "$newdir"
        cd "$newdir"
        jar xvf "$src"
    elif [[ "$name" == *.tar.bz2 ]];
    then
        mkdir -p "$newdir"
        cd "$newdir"
        tar xjvf "$src"
    elif [[ "$name" == *.tar.gz ]];
    then
        mkdir -p "$newdir"
        cd "$newdir"
        tar xzvf "$src"
    elif [[ "$name" == *.gz ]];
    then
        mkdir -p "$newdir"
        cd "$newdir"
        tar xzvf "$src"
    elif [[ "$name" == *.tar ]];
    then
        mkdir -p "$newdir"
        cd "$newdir"
        tar xvf "$src"
    elif [[ "$name" == *.zip ]];
    then
        mkdir -p "$newdir"
        cd "$newdir"
        jar xvf "$src"
    elif [[ "$name" == *.rar ]];
    then
        mkdir -p "$newdir"
        cd "$newdir"
        unrar x "$src"
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

