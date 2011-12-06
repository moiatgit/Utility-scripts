find ~/.thumbnails/normal/  -type f -exec rm -v '{}' \;
find ~/.thumbnails/large/  -type f -exec rm -v '{}' \;
find ~/.thumbnails/fail/gnome-thumbnail-factory/  -type f -exec rm -v '{}' \;
python ~/bin/netejarecent.py -a
