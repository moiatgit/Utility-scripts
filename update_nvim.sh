#! /bin/bash
mkdir -p $HOME/soft/nvim.versions
cd $HOME/soft/nvim.versions
if [[ "$1" == "nightly" ]];
then
    version=nightly
else
    version=stable
fi

echo "neovim upgrader to $version"

mkdir -p $version
cd $version
curl -LO https://github.com/neovim/neovim/releases/download/$version/nvim.appimage
chmod u+x nvim.appimage

ln -f -s -r $(realpath nvim.appimage) $HOME/soft/nvim
