#! /bin/bash

echo "Utility to decrypt files using aes-256"

if [ -f "$1" -a -n "$2" -a ! -f "$2" ];
then
    openssl aes-256-cbc -d -in "$1" -out "$2"
    if [ $? -ne 0 ];
    then
        echo "Decryption error"
    fi
else
    echo "Usage: $0 existingfiletodecrypt nonexistingoutputfile"
fi

