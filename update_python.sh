#! /bin/bash
echo "This script updates python"
if [ -z "$1" ];
then
    echo "Use $0 download-url | downloaded_file"
    echo "\te.g. $0 https://www.python.org/ftp/python/3.11.1/Python-3.11.1.tgz"
    echo "\te.g. $0 3.11.1"
    exit 1
fi

if [[ "$1" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]];
then
    url="https://www.python.org/ftp/python/$1/Python-$1.tar.xz"
elif [ -f "$1" ];
then
    zipped="$1"
else
    url="$1"
fi
if [ -z "$zipped" ];
then
    cd ${TMPDIR:-/tmp}
    if ! wget -c "$url";
    then
        echo "Error downloading $url"
        exit 1
    fi
    zipped=$(basename "$url")
    if [ ! -f $zipped ];
    then
        echo "Error: downloaded file not found $zipped"
        exit 1
    fi
fi
echo "zipped $zipped"

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

# Ensure dependencies
sudo apt install -y \
  build-essential \
  pkg-config \
  libffi-dev \
  libssl-dev \
  zlib1g-dev \
  libbz2-dev \
  libreadline-dev \
  libsqlite3-dev \
  libncursesw5-dev \
  xz-utils \
  tk-dev \
  libxml2-dev \
  libxmlsec1-dev \
  liblzma-dev \
  libgdbm-dev \
  libgdbm-compat-dev \
  libnss3-dev \
  libedit-dev \
  uuid-dev \
  libyaml-dev

# Do compile

./configure --enable-optimizations --with-lto=full \
                                   --enable-shared --with-system-libffi \
                                   --with-ensurepip=upgrade && \
    make -j $(nproc) && \
    sudo make altinstall
