#! /bin/bash
#
# This script sets the keybindings on dconf
#
dconf load /org/gnome/desktop/wm/keybindings/ << END
[/]
cycle-windows=['<Super><shift>j']
cycle-windows-backward=['<Super><shift>k']
lower=@as []
maximize=['<Super>KP_5']
maximize-horizontally=['<Super>KP_6', '<Super>h']
maximize-vertically=['<Super>KP_8', '<Super>v']
minimize=['<Super>KP_0', '<Super>comma']
move-to-center=@as ['<Super>k']
move-to-corner-ne=['<Super>KP_9', '<Super>o']
move-to-corner-nw=['<Super>KP_7', '<Super>u']
move-to-corner-se=['<Super>KP_3', '<Super>l']
move-to-corner-sw=['<Super>KP_1', '<Super>j']
move-to-side-e=@as []
move-to-side-n=@as []
move-to-side-s=@as []
move-to-side-w=@as []
move-to-workspace-1=['<Super><shift>1']
move-to-workspace-10=['<Super><shift>0']
move-to-workspace-2=['<Super><shift>2']
move-to-workspace-3=['<Super><shift>3']
move-to-workspace-4=['<Super><shift>4']
move-to-workspace-5=['<Super><shift>5']
move-to-workspace-6=['<Super><shift>6']
move-to-workspace-7=['<Super><shift>7']
move-to-workspace-8=['<Super><shift>8']
move-to-workspace-9=['<Super><shift>9']
panel-run-dialog=['<Alt>F2', '<Super>r']
switch-group=['<Alt>masculine']
switch-to-workspace-1=['<Super>1']
switch-to-workspace-10=['<Super>0']
switch-to-workspace-2=['<Super>2']
switch-to-workspace-3=['<Super>3']
switch-to-workspace-4=['<Super>4']
switch-to-workspace-5=['<Super>5']
switch-to-workspace-6=['<Super>6']
switch-to-workspace-7=['<Super>7']
switch-to-workspace-8=['<Super>8']
switch-to-workspace-9=['<Super>9']
toggle-maximized=@as ['<Super>m']
unmaximize=['<Super>KP_2']
END
if [ "$?" -eq 0 ];
then
    echo "Done"
else
    echo "There was a problem when trying to set the configuration"
fi

