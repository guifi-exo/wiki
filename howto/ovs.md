# Open Virtual Switch

open virtual switch enables faster communications than the by default linux controller

important note: ovs in debian stretch stable is buggy (I get "unable to raise network interfaces" with an awesome timeout of 5 minutes). But with [proxmox repos](https://pve.proxmox.com/wiki/Install_Proxmox_VE_on_Debian_Stretch#Adapt_your_sources.list) you will not have any problem

requirements:

    apt-get install net-tools openvswitch-switch

consider two interfaces named eno1 and eno2

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [Bonding active/backup between two interfaces](#bonding-active/backup-between-two-interfaces)
- [Bonding LACP between two interfaces](#bonding-lacp-between-two-interfaces)
- [One physical network interface (no bonding)](#one-physical-network-interface-no-bonding)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Bonding active/backup between two interfaces

Active/standby failover mode is where one of the ports in the link aggregation port is active and all others are in standby mode. One MAC address (MAC address of the active link) is used as the MAC address of the aggregated link.

```
source /etc/network/interfaces.d/*

auto lo
iface lo inet loopback

allow-vmbr0 bond0
iface bond0 inet manual
  ovs_bonds   eno1 eno2
  ovs_type    OVSBond
  ovs_bridge  vmbr0
  ovs_options bond_mode=active-backup

allow-ovs vmbr0

auto vmbr0
iface vmbr0 inet manual
  ovs_type  OVSBridge
  ovs_ports bond0 iface1 iface2 iface3

allow-vmbr0 iface1
iface temp inet static
  address     10.1.1.2
  netmask     255.255.255.0
  gateway     10.1.1.1
  ovs_type    OVSIntPort
  ovs_bridge  vmbr0

allow-vmbr0 iface2
iface pve inet static
  address     192.168.10.2
  netmask     255.255.255.0
  ovs_type    OVSIntPort
  ovs_bridge  vmbr0
  ovs_options tag=10

allow-vmbr0 iface3
iface gfs inet static
  address     192.168.15.2
  netmask     255.255.255.0
  ovs_type    OVSIntPort
  ovs_bridge  vmbr0
  ovs_options tag=15

```

## Bonding LACP between two interfaces

Important note: this REQUIRES setting LACP in switch

It performs load-balancing between the bonded interfaces. In `balance-tcp` mode, it uses 5-tuple (source and destination IP, source and destination port, protocol) to balance traffic across the ports in an aggregated link. In `balance-slb` uses a simple hashing algorithm on source MAC and VLAN to choose the port in an aggregated link to forward the traffic.

```
source /etc/network/interfaces.d/*

auto lo
iface lo inet loopback

allow-vmbr0 bond0
iface bond0 inet manual
  ovs_bonds   eno1 eno2
  ovs_type    OVSBond
  ovs_bridge  vmbr0
  ovs_options lacp=active other_config:lacp-time=fast bond_mode=balance-tcp

allow-ovs vmbr0

auto vmbr0
iface vmbr0 inet manual
  ovs_type  OVSBridge
  ovs_ports bond0 iface1 iface2 iface3

allow-vmbr0 iface1
iface temp inet static
  address     10.1.1.2
  netmask     255.255.255.0
  gateway     10.1.1.1
  ovs_type    OVSIntPort
  ovs_bridge  vmbr0

allow-vmbr0 iface2
iface pve inet static
  address     192.168.10.2
  netmask     255.255.255.0
  ovs_type    OVSIntPort
  ovs_bridge  vmbr0
  ovs_options tag=10

allow-vmbr0 iface3
iface gfs inet static
  address     192.168.15.2
  netmask     255.255.255.0
  ovs_type    OVSIntPort
  ovs_bridge  vmbr0
  ovs_options tag=15

```

## One physical network interface (no bonding)

{You only want / you only have} one ethernet interface

```
source /etc/network/interfaces.d/*

auto lo
iface lo inet loopback

allow-vmbr0 eno1
iface eno1 inet manual
  ovs_type OVSPort
  ovs_bridge vmbr0

allow-ovs vmbr0

auto vmbr0
iface vmbr0 inet manual
        ovs_type  OVSBridge
        ovs_ports eno1 iface1 iface2 iface3

allow-vmbr0 iface1
iface temp inet static
  address     10.1.1.2
  netmask     255.255.255.0
  gateway     10.1.1.1
  ovs_type    OVSIntPort
  ovs_bridge  vmbr0

allow-vmbr0 iface2
iface pve inet static
  address     192.168.10.2
  netmask     255.255.255.0
  ovs_type    OVSIntPort
  ovs_bridge  vmbr0
  ovs_options tag=10

allow-vmbr0 iface3
iface gfs inet static
  address     192.168.15.2
  netmask     255.255.255.0
  ovs_type    OVSIntPort
  ovs_bridge  vmbr0
  ovs_options tag=15
```
