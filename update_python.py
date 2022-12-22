#! /bin/bash
echo "This script updates python"
if [ -z "$1" ];
then
    echo "Use $0 download-url"
    echo "\t e.g. $0 https://www.python.org/downloads/release/python-3111/"
exit 1
fi
zipped=$(basename $1)
foldername=${zipped%.*}
echo $foldername
cd /tmp
if ! wget -c "$1";
then
    echo "Error downloading $1"
    exit 1
fi
if [! -f $zipped ];
then
    echo "Error: downloaded file not found $zipped"
    exit 1
fi
if [ ! -d $foldername ];
then 
    tar xzvf $zipped
fi
if [ ! -d $foldername ];
then
    echo "Error: expected folder name $foldername"
    exit 1
fi
cd $foldername
if [ ! -f configure ];
then
    echo "Error: expected file $foldername/configure"
    exit 1
fi
./configure --enable-optimizations && \
    make -j `nproc` && \
    sudo make altinstall
