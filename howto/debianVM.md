<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [Default credentials (change)](#default-credentials-change)
- [Persistent firewall](#persistent-firewall)
  - [IPv4](#ipv4)
  - [IPv6](#ipv6)
  - [Config file](#config-file)
  - [IPv4 vs IPv6](#ipv4-vs-ipv6)
- [Installed applications and related config](#installed-applications-and-related-config)
- [APT sources](#apt-sources)
- [Resource policy](#resource-policy)
- [Disk policy](#disk-policy)
  - [Create](#create)
    - [Regular disk](#regular-disk)
    - [Swap](#swap)
  - [Resize](#resize)
    - [Root](#root)
    - [Regular disk](#regular-disk-1)
    - [Swap](#swap-1)
  - [Checkers](#checkers)
- [Kernel options](#kernel-options)
  - [network interfaces](#network-interfaces)
  - [I want to know what's going on](#i-want-to-know-whats-going-on)
  - [novnc proxmox resize issue](#novnc-proxmox-resize-issue)
  - [summary: all kernel options](#summary-all-kernel-options)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

debian server template and operations

# Default credentials (change)

- hostname: host
- user: user (without sudo). root account activated
- password: debian

# Persistent firewall

src https://wiki.debian.org/iptables

## IPv4

init persistent firewall4:

```
cat > /etc/network/if-pre-up.d/firewall4 <<EOF
#!/bin/sh
/sbin/iptables-restore < /etc/firewall4
EOF
chmod +x /etc/network/if-pre-up.d/firewall4
```

save current rules: `iptables-save > /etc/firewall4`

load current rules: `iptables-restore < /etc/firewall4`

## IPv6

init persistent firewall6:

```
cat > /etc/network/if-pre-up.d/firewall6 <<EOF
#!/bin/sh
/sbin/ip6tables-restore < /etc/firewall6
EOF
chmod +x /etc/network/if-pre-up.d/firewall6
```

save current rules: `ip6tables-save > /etc/firewall4`

load current rules: `ip6tables-restore < /etc/firewall4`

## Config file

init with empty content (thanks https://unix.stackexchange.com/questions/88490/how-do-you-use-output-redirection-in-combination-with-here-documents-and-cat)

```
cat <<EOF | tee /etc/firewall4 /etc/firewall6 &> /dev/null
*mangle
# content about mangle (?) mss tcp?
COMMIT

*filter
# input, output or forward
COMMIT

*nat
# content about nat: dest nat, src nat or masquerade
COMMIT
EOF
```

example with comment

```
*nat
# content about nat: dest nat, src nat or masquerade
-A POSTROUTING -o eth0 -j MASQUERADE -m comment --comment "from VPN access to guifi"
COMMIT
```

## IPv4 vs IPv6

| IPv4 | IPv6 |
| ---- | ---- |
| `-p icmp` | `-p ipv6-icmp` |

# Installed applications and related config

`apt-get install vim tmux screen`

VIM: disable mouse -> src http://blackhold.nusepas.com/2016/12/04/vim-en-debian-9-al-seleccionar-se-pone-en-modo-visual/

# APT sources

```
deb http://deb.debian.org/debian/ stretch main
deb-src http://deb.debian.org/debian/ stretch main

deb http://security.debian.org/debian-security stretch/updates main
deb-src http://security.debian.org/debian-security stretch/updates main

# stretch-updates, previously known as 'volatile'
deb http://deb.debian.org/debian/ stretch-updates main
deb-src http://deb.debian.org/debian/ stretch-updates main
```

# Resource policy

types of VM:
- default VM (debian) 1 GB RAM, 4 GB storage, 1 core
- router VM. 512 MB RAM, 2 GB storage, 1 core
  - src mikrotik https://wiki.mikrotik.com/wiki/Manual:CHR#System_Requirements
  - src vyos https://wiki.vyos.net/wiki/User_Guide#Installation

storage options:
- qcow2
- virtio
- writeback

cpu options: `host` (use instead `kvm64` if you have High Availability and you want to perform hot migrations)

ram options:
- uncheck ballooning [discussion required] enabled by default by proxmox. but disabled at the moment

network options:
- virtio

# Disk policy

VMs start with a virtio disk with a qcow2 writeback of 4 GB with a msdos partition table and a root partition in `/dev/vda`, no swap. This root partition use xfs. Through this automated [debian preseed installer](https://TODO)

## Create

Expected creations:
- Create new disk
- Create new mountpoint, examples: /tmp, /var, /home
- Create new swap


In all this cases start with a disk of 2 GB and use it entirely without defining a msdos partition table.

xfs is recommended, format it this way:

`mkfs.xfs /dev/vdb`

add it to `/etc/fstab`

note: root is already created

### Regular disk

if is a regular disk, for example, `/dev/vdb` that mounts `/tmp`:

`echo UUID=$(blkid -s UUID -o value /dev/vdb) /tmp xfs defaults 0 0 >> /etc/fstab`

`mount -a`

check filesystem is there with `df -h`

### Swap

if is swap:

```
echo UUID=$(blkid -s UUID -o value /dev/vdb) none swap sw 0 0 >> /etc/fstab`
mkswap /dev/vdb
swapon -a
```
## Resize

### Root

The first operation is to resize the disk using proxmox, after that you require to put some commands depending on purpose on that disk

resize disk when is a root partition at /dev/vda1

```
# sometimes this command is required to force kernel update partition table
#partprobe /dev/vda
parted /dev/vda resizepart 1 Yes 100%
# alternatively
# parted /dev/vda resizepart 1 Yes -1
xfs_growfs /dev/vda1
```

### Regular disk

resize disk when is a regular disk (assuming a mounted xfs disk), directly:

`xfs_grow /path/to/mounted/disk`

### Swap

resize disk when is for swap:

```
swapoff -a
mkswap -U $(blkid -s UUID -o value /dev/vdb) /dev/vdb
swapon -a
```
## Checkers

Disks:

disk resize is showed in kernel log: `dmesg | tail` or `tailf /var/log/messages`

with `parted /dev/vda p` you can see the size of the disk and the size of the partition

with `df -h` you can see the size of the filesystem


Swap:

`swapon -s` or `free -h`

# Kernel options

This section describes tricks I had to do in debian 8 to debian 9 migrations related to linux kernel

## network interfaces

It's not clear for me why the change of interface names, but for some time I will maintain old style

add options:

    net.ifnames=0

    biosdevname=0

## I want to know what's going on

I always change default option of 'quiet' to 'verbose'. This makes boot a little bit slower, but if something is strange, I can see it in boot time easily (fast boot =>try to do a video and watch slowly)

## novnc proxmox resize issue

Got accostumated to the tiny proxmox novnc console in virtual machines. After some upgrade, it starts ok, but after boot line:

    fbcon: bochsdrmfb (fb0) is primary interface

it resizes. Grr!

You can avoid that adding to `/etc/default/grub` option `bochs_drm.fbdev=off` src https://unix.stackexchange.com/questions/346090/disable-framebuffer-in-qemu-guests

## summary: all kernel options

`GRUB_CMDLINE_LINUX_DEFAULT="net.ifnames=0 biosdevname=0 verbose bochs_drm.fbdev=off"`
