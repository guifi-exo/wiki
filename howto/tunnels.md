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

## L2TP

(Configuració L2TP)[l2tp-configuration.md]

algunes de les seves avantatges

- és de tipus dial-up
    - és molt fàcil de configurar (usuari, contraseña), tant per la banda de client com de operador
    - per la banda de operador, a més a més, et permet fer gestió professional dels usuaris. Amb IPIP s'han de fer inventillos. L2TP es presta més a un eina de gestió bonica per manegar usuaris-tunels (radius, LDAP)
- es poden canviar les característiques associades al tunel: ara li poso un altre IP4, o li trec IPv6, ara el dono de baixa
- el pots moure de lloc sense demanar permís (IPIP s'ha de saber la IP d'origen)
- el pots posar contra un router que faci NAT, té tècniques de NAT traversal que IPIP i GRE no tenen
pots posar xifratge al tunel. això està en recerca, qui ho vulgui investigar...

## Encrypted tunnels

Someone tested the maximum bandwidth from encrypted Tincd, Fastd and Wireguard and the best results were with Wireguard
there's some more people in Freifunk testing it: https://forum.freifunk.net/t/wireguard-als-zukuenftige-vpn-loesung/12858

try/test softether.org

https://justus.berlin/2016/02/performance-of-tunneling-methods-in-openwrt/

issue/discussion on libremesh: https://github.com/libremesh/lime-packages/issues/99
