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

extract() {
    # checks whether the folder $1 already exists. If not, it creates it
    # and extracts $3 file with $2 command inside the new folder
    newdir=$1
    command=$2
    src=$3
    if [ -d "$newdir" ];
    then
        echo "Folder $newdir already exists: no action"
    else
        mkdir -p "$newdir"
        cd "$newdir"
        eval $command \"$src\"
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

SAVEIFS=$IFS
IFS=$(echo -en "\n\b")
#files=`find . -type f \( -name '*.zip' -o -name '*.tar.gz' -o -name '*.jar' \)`
files=`find . -type f`
for f in $files;
do
    processa "$f"
done
IFS=$SAVEIFS

