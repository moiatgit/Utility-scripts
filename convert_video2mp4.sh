#! /bin/bash
# Dependences: HandBrakeCLI

echo "This script converts videos in current folder into mp4"

for i in *;
do
    extension="${i##*.}"
    if [[ "$extension" == "m4v" || "$extension" == "webm" || "$extension" == "mkv" || "$extension" == "m4v" || "$extension" == "mov" || "$extension" == "mpg" ]];
    then
        name="${i%.*}"
        if [ ! -f "$name.mp4" ];
        then
            echo "Lets go for $name"
            nice HandBrakeCLI -i "$i" -o "$name.mp4"
        fi
    fi
done


# Here a script that converted the files from a temporary folder
# to a main profile
#for f in $*;
#do
#    for i in $f/*.mp4;
#    do
#        echo $i
#        nom=`basename "$i"`
#        nice HandBrakeCLI -i "$i" -o "$nom" --encoder-profile main
#        nice mv -v "$nom" "$i"
#    done
#done
#
