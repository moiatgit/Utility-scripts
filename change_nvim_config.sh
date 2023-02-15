#! /bin/bash

echo "This script changes the configuration of nvim"

if [ -z "$1" ];
then
    config="nvim.standard"
else
    config="$1"
fi

if [ ! -d "$HOME/.config/$config" ];
then
    echo "ERROR: config not found at ~/.config"
    exit 1
fi

if [ ! -d "$HOME/.local/share/$config" ];
then
    echo "ERROR: config not found at ~/.local/share"
    exit 1
fi

echo "It will change the configuration to $config"
echo "ctrl-c to abort"
read resposta

cd $HOME/.config/
rm nvim
ln -s "$config" nvim
cd $HOME/.local/share
rm nvim
ln -s "$config" nvim

echo "Done"
