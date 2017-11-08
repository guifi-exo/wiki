# Tunnels
- GRE kernel module (Generic Routing Encapsulation) [kernelspace] [no xifrat]
- OpenVPN [userspace] [xifrat]

## GRE

Tested on Debian 9 Stretch, as root:

```
echo <<EOF > /etc/network/if-up.d/exo
#! /bin/sh
guifi_IP=x.x.x.x
inet_IP=y.y.y.y
exo_IP=10.38.140.225

ip tunnel add exo mode gre remote "$exo_IP" local "$guifi_IP" ttl 255
# src http://brezular.com/2015/09/29/gre-tunnel-between-cisco-and-linux/
ip link set exo mtu 1400
ip link set exo up
ip a a "$inet_IP"/32 dev exo
ip r a 0.0.0.0/0 via "$inet_IP"
EOF

reboot
```

## PPPoE

requirement: an interface prepared to transmit pppoe

apt-get install pppoeconf

pppoeconf

## Encrypted tunnels

Someone tested the maximum bandwidth from encrypted Tincd, Fastd and Wireguard and the best results were with Wireguard
there's some more people in Freifunk testing it: https://forum.freifunk.net/t/wireguard-als-zukuenftige-vpn-loesung/12858

try/test softether.org

https://justus.berlin/2016/02/performance-of-tunneling-methods-in-openwrt/
