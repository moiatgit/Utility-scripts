# This script prepares a complete new installation
# it requires sudo privileges

sudo apt install git
sudo apt install vim vim-gui-common
sudo apt install dconf-editor
sudo apt install tree
sudo apt install graphviz

# for python3 compilation
sudo apt install python3-pip
sudo apt install build-essential zlib1g-dev libncurses5-dev libgdm-dev
libnss3-dev libssl-dev libreadline-dev libffi-dev wget
sudo apt install libsqlite3-dev
sudo apt install libbz2-dev
sudo apt install python3-tk tk tk-dev libffi-dev

#if [ ! -d $HOME/bin ];
#then
#	git clone https://github.com/moiatgit/Utility-scripts $HOME/bin
#fi
#bash $HOME/bin/set_keybindings.sh
#
#gsettings set org.gnome.mutter dynamic-workspaces false
#gsettings set org.gnome.desktop.wm.preferences num-workspaces 10
#gsettings set org.gnome.shell.app-switcher current-workspace-only true


sudo apt install libcanberra-gtk-module
