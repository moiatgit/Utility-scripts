#! /bin/bash
echo "This script updates python"
if [ ! -f configure ];
then
    echo "First of all, download and untar the new version"
    echo "Then cd into the new folder and rerun this script"
else
    ./configure --enable-optimizations && \
        make -j `nproc` && \
        sudo make altinstall
fi

