#! /bin/bash
if [ -z "$1" ];
then
    owner=test
else
    owner=$1
fi
echo "This script restricts user $owner access to different resources"
echo "It requires sudo privileges"
sudo iptables -I OUTPUT -m owner --uid-owner $owner -j DROP
#sudo iptables -I OUTPUT -p tcp -m owner --uid-owner $owner -j DROP
#sudo iptables -I OUTPUT -p udp -m owner --uid-owner $owner -j DROP
#sudo iptables -I OUTPUT -p icmp -m owner --uid-owner $owner -j DROP
