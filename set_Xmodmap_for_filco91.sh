#! /bin/bash
Xmodmapfile="$HOME/.Xmodmap" 
echo "Sets the ~/.Xmodmap file to remap Filco's keys"
if [ -f "$Xmodmapfile" ];
then
    echo "File $Xmodmapfile already exists. No changes"
else
    cat > "$Xmodmapfile" << END
keycode 102 = ISO_Level3_Shift
keycode 100 = ISO_Level3_Shift
keycode 101 = Super_R NoSymbol Super_R
END
    echo "$Xmodmapfile has been created"
fi
