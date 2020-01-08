#! /bin/bash
echo "This script restricts user access to different resources"
echo "It requires sudo privileges"
sudo iptables -I OUTPUT -p tcp -m owner --uid-owner test -j DROP
sudo iptables -I OUTPUT -p udp -m owner --uid-owner test -j DROP
sudo iptables -I OUTPUT -p icmp -m owner --uid-owner test -j DROP
