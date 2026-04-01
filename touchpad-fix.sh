#! /bin/sh
echo "Reset mouse config: one finger moves"
sudo modprobe -r psmouse
sudo modprobe psmouse
