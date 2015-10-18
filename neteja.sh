echo "Cleaning temporary files"
find ~/.thumbnails/  -type f -exec rm -v '{}' \;
rm -rvf ~/.local/share/Trash/*
#python ~/bin/netejarecent.py -a
echo "Cleaning done!"
