#!/bin/sh
mkdir -p ~/.config/contrasuenyes
cd ~/.config/contrasuenyes
if [ -f .contrasuenyes ]; then
  mv .contrasuenyes ".contrasuenyes.$(date +%Y%m%d%H%M%S)"
fi
scp "blami.home:~/.config/contrasuenyes/.contrasuenyes" .
