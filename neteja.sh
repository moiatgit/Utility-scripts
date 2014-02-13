echo "Cleaning temporary files"
find ~/.thumbnails/  -type f -exec rm -v '{}' \;
python ~/bin/netejarecent.py -a
echo "Cleaning done!"
