echo "Cleaning temporary files"
find ~/.thumbnails/  -type f -exec rm -v '{}' \;
rm -rvf ~/.local/share/Trash/*
#python ~/bin/netejarecent.py -a
find ~/.cache/shotwell -type f -exec rm -v {} \;
find ~/.cache/thumbnails  -type f -exec rm -v '{}' \;
echo "Cleaning done!"
