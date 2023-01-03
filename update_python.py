#! /bin/bash
echo "This script updates python"
if [ -z "$1" ];
then
    echo "Use $0 download-url"
    echo "\te.g. $0 https://www.python.org/ftp/python/3.11.1/Python-3.11.1.tgz"
exit 1
fi
zipped=$(basename $1)
foldername=${zipped%.*}
echo $foldername
cd ${TMPDIR:-/tmp}
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
