#! /usr/bin/bash
# This script sets my gnome3 preferences
#
# Sets the shortcuts to access the different workspaces
gsettings set org.gnome.desktop.wm.preferences num-workspaces 10
#
gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-1  "['<Ctrl><Super>1']"
gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-2  "['<Ctrl><Super>2']"
gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-3  "['<Ctrl><Super>3']"
gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-4  "['<Ctrl><Super>4']"
gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-5  "['<Ctrl><Super>5']"
gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-6  "['<Ctrl><Super>6']"
gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-7  "['<Ctrl><Super>7']"
gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-8  "['<Ctrl><Super>8']"
gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-9  "['<Ctrl><Super>9']"
gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-10 "['<Ctrl><Super>0']"

gsettings set org.gnome.desktop.wm.keybindings move-to-workspace-1  "['<Super><Shift>1']"
gsettings set org.gnome.desktop.wm.keybindings move-to-workspace-2  "['<Super><Shift>2']"
gsettings set org.gnome.desktop.wm.keybindings move-to-workspace-3  "['<Super><Shift>3']"
gsettings set org.gnome.desktop.wm.keybindings move-to-workspace-4  "['<Super><Shift>4']"
gsettings set org.gnome.desktop.wm.keybindings move-to-workspace-5  "['<Super><Shift>5']"
gsettings set org.gnome.desktop.wm.keybindings move-to-workspace-6  "['<Super><Shift>6']"
gsettings set org.gnome.desktop.wm.keybindings move-to-workspace-7  "['<Super><Shift>7']"
gsettings set org.gnome.desktop.wm.keybindings move-to-workspace-8  "['<Super><Shift>8']"
gsettings set org.gnome.desktop.wm.keybindings move-to-workspace-9  "['<Super><Shift>9']"
gsettings set org.gnome.desktop.wm.keybindings move-to-workspace-10 "['<Super><Shift>0']"

# disable animations
gsettings set org.gnome.desktop.interface enable-animations false

# improve clock
gsettings set org.gnome.desktop.interface clock-show-weekday true
gsettings set org.gnome.desktop.interface clock-show-seconds true

# hot corners
gsettings set org.gnome.desktop.interface enable-hot-corners false

# menubar detachable
gsettings set org.gnome.desktop.interface menubar-detachable false
