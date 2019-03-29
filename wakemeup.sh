#! /bin/bash
defaulttime=10m
timetowait=${1:-$defaulttime}
echo "This script will play a sound after $timetowait"
$(sleep $timetowait; paplay bell.wav) &
