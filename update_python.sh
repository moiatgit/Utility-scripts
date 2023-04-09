#! /bin/bash
echo "This script updates python"
if [ -z "$1" ];
then
    echo "Use $0 download-url | downloaded_file"
    echo "\te.g. $0 https://www.python.org/ftp/python/3.11.1/Python-3.11.1.tgz"
exit 1
fi
zipped=$(basename "$1")
if [[ "$zipped" == *.tar.gz ]];
then
    foldername=$(basename "$zipped" .tar.gz)
    taroption=xzvf
elif [[ "$zipped" == *.tgz ]];
then
    foldername=$(basename "$zipped" .tgz)
    taroption=xzvf
elif [[ "$zipped" == *.tar.xz ]];
then
    foldername=$(basename "$zipped" .tar.xz)
    taroption=xJvf
else
    echo "Not prepared for this kind of file: $zipped"
    exit 1
fi
echo "foldername $foldername"

if [ ! -f $zipped ];
then
    cd ${TMPDIR:-/tmp}
    if ! wget -c "$1";
    then
        echo "Error downloading $1"
        exit 1
    fi
fi
if [ ! -f $zipped ];
then
    echo "Error: downloaded file not found $zipped"
    exit 1
fi
if [ ! -d $foldername ];
then 
    tar $taroption "$zipped"
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
