#! /bin/bash
basedir=$(dirname $0)
soundfilename=bell.wav
defaulttime=10m
timetowait=${1:-$defaulttime}
paplay "$basedir/$soundfilename"
echo "This script will play a sound after $timetowait"
$(sleep $timetowait; paplay "$basedir/$soundfilename") &
