# open virtual switch

open virtual switch enables faster communications than the by default linux controller

important note: ovs in debian stretch stable is buggy (I get "unable to raise network interfaces" with an awesome timeout of 5 minutes). But with [proxmox repos](https://pve.proxmox.com/wiki/Install_Proxmox_VE_on_Debian_Stretch#Adapt_your_sources.list) you will not have any problem

requirements:

    apt-get install net-tools openvswitch-switch

consider two interfaces named eno1 and eno2

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [bond backup between two interfaces](#bond-backup-between-two-interfaces)
- [bond lacp between two interfaces](#bond-lacp-between-two-interfaces)
- [one physical network interface (no bond)](#one-physical-network-interface-no-bond)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## bond backup between two interfaces

You have two ethernet interfaces and you don't know what to do? You can bound them to increase redundancy

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

## bond lacp between two interfaces

Important note: this REQUIRES setting LACP in switch

This does redundancy ethernet and your bandwidth is increased in a (I think) round robin style

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

## one physical network interface (no bond)

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
