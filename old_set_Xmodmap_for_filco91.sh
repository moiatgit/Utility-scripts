#! /bin/bash
echo "Sets the ~/.Xmodmap file to remap Filco's keys"
if [[ "$1" == "!" ]];
then
    echo "Es procedeix a executar els remappings directament per a aquesta sessió"
    xmodmap -e "keycode 102 = ISO_Level3_Shift"
    xmodmap -e "keycode 100 = ISO_Level3_Shift"
    xmodmap -e "keycode 101 = Super_L"
    echo "Fet!"
    exit
fi
if [[ "$1" == "f" ]];
then
    Xmodmapfile="$HOME/.Xmodmap" 
    echo "Es procedeix a crear els mappings al fitxer $Xmodmapfile"
    if [ -f "$Xmodmapfile" ];
    then
        echo "File $Xmodmapfile already exists. No changes"
    else
        cat > "$Xmodmapfile" << END
keycode 102 = ISO_Level3_Shift
keycode 100 = ISO_Level3_Shift
keycode 101 = Super_L
END
        echo "$Xmodmapfile has been created"
    fi
    exit
fi
echo "Indica amb l'argument ! per realitzar el mapping o f per crear el fitxer"

