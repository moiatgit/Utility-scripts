#! /bin/bash
# Dependences: HandBrakeCLI

echo "This script converts videos in current folder into mp4"

for i in *;
do
    extension="${i##*.}"
    if [[ "$extension" == "m4v" || "$extension" == "webm" || "$extension" == "mkv" ]];
    then
        name=`echo $i | cut -d'.' -f1`;
        if [ ! -f "$name.mp4" ];
        then
            HandBrakeCLI -i "$i" -o "$name.mp4"
        fi
    fi
done
