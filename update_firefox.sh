#! /bin/bash
# Updates firefox: it suposes you've installed it manually following for
# example
# https://linuxconfig.org/how-to-install-latest-firefox-browser-on-debian-9-stretch-linux"


# To recover original version
# sudo unlink /usr/lib/firefox-esr/firefox-esr
# sudo mv /usr/lib/firefox-esr/firefox-esr_orig /usr/lib/firefox-esr/firefox-esr

echo "Updates firefox when installed manually. In case of doubt, please abort this script"
read resposta
cd /tmp
sudo wget -O FirefoxSetup.tar.bz2 "https://download.mozilla.org/?product=firefox-latest&os=linux64&lang=en-US"
sudo tar xjf FirefoxSetup.tar.bz2 -C /opt/firefox/
