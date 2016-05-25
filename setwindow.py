#!/usr/bin/env python3

# Following indications from: http://askubuntu.com/questions/613973/how-can-i-start-up-an-application-with-a-pre-defined-window-size-and-position

# This script aims to define position and size of windows to open
# it requires wmctrl and xdotool packages installed

# Example of usage:
# in .bash_aliases add the following line:
#   alias gvim='$HOME/bin/setwindow.py 0 0 50 95 gvim -p'
# This will open gvim starting at left-top with size 50% width and 95% height

import subprocess
import time
import sys

hpos = sys.argv[1]
vpos = sys.argv[2]
hsize = sys.argv[3]
vsize = sys.argv[4]
app = " ".join(sys.argv[5:])

get = lambda x: subprocess.check_output(["/bin/bash", "-c", x]).decode("utf-8")
ws1 = get("wmctrl -lp"); t = 0
subprocess.Popen(["/bin/bash", "-c", app])

while t < 30:
    ws2 = [w.split()[0:3] for w in get("wmctrl -lp").splitlines() if not w in ws1]
    procs = [[(p, w[0]) for p in get("ps -e ww").splitlines() \
              if app in p and w[2] in p] for w in ws2]
    if len(procs) > 0:
        w_id = procs[0][0][1]
        cmd1 = "wmctrl -ir "+w_id+" -b remove,maximized_horz"
        cmd2 = "wmctrl -ir "+w_id+" -b remove,maximized_vert"
        cmd3 = "xdotool windowsize --sync "+procs[0][0][1]+" "+hsize+"% "+vsize+"%"
        cmd4 = "xdotool windowmove "+procs[0][0][1]+" "+hpos+" "+vpos
        for cmd in [cmd1, cmd2, cmd3, cmd4]:
            subprocess.call(["/bin/bash", "-c", cmd])
        break
    time.sleep(0.5)
    t = t+1
