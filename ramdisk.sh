#! /bin/bash

# This script mounts a RAM disk of $1 size (by default 1G)
# It requires sudo privileges

default_size="1G"
default_location=/tmp/ramdisk
size=${1:-$default_size}
location=${2:-$default_location}
echo "Usage: $0 [size [location]]"
echo "This script will mount a RAM disk of $size on $location"
echo "press enter to continue <ctrl>-c to cancel"
read resposta


sudo mkdir -p /tmp/ramdisk
sudo chmod 777 /tmp/ramdisk

sudo mount -t tmpfs -o size=$size myramdisk $location
