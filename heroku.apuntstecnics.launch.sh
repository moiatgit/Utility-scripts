#! /bin/bash

echo "Use this script to launch a http server for 'apunts tècnics'"
echo "press a key to continue <ctrl>-c to cancel"
read resposta

cd ~/Feina/heroku.apuntstecnics
python -m SimpleHTTPServer
