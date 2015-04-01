#! /bin/bash
#
# This script sets the keybindings on dconf
#
dconf load /org/gnome/desktop/wm/keybindings/ << END
[/]
cycle-windows=['<Super>j']
cycle-windows-backward=['<Super>k']
lower=@as []
maximize=['<Super>KP_5', '<Super><ctrl>comma']
maximize-horizontally=['<Super>KP_6', '<Super><ctrl>k']
maximize-vertically=['<Super>KP_8', '<Super><ctrl>i']
minimize=['<Super>KP_0']
move-to-center=@as []
move-to-corner-ne=['<Super>KP_9', '<Super><ctrl>o']
move-to-corner-nw=['<Super>KP_7', '<Super><ctrl>u']
move-to-corner-se=['<Super>KP_3', '<Super><ctrl>l']
move-to-corner-sw=['<Super>KP_1', '<Super><ctrl>j']
move-to-side-e=@as []
move-to-side-n=@as []
move-to-side-s=@as []
move-to-side-w=@as []
move-to-workspace-1=['<super><shift>1']
move-to-workspace-10=['<super><shift>0']
move-to-workspace-2=['<super><shift>2']
move-to-workspace-3=['<super><shift>3']
move-to-workspace-4=['<super><shift>4']
move-to-workspace-5=['<super><shift>5']
move-to-workspace-6=['<super><shift>6']
move-to-workspace-7=['<super><shift>7']
move-to-workspace-8=['<super><shift>8']
move-to-workspace-9=['<super><shift>9']
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
toggle-maximized=@as []
unmaximize=['<Super>KP_2']
END
if [ "$?" -eq 0 ];
then
    echo "Done"
else
    echo "There was a problem when trying to set the configuration"
fi

