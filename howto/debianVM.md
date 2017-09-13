<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [network interfaces](#network-interfaces)
- [I want to know what's going on](#i-want-to-know-whats-going-on)
- [novnc proxmox resize issue](#novnc-proxmox-resize-issue)
- [summary: all options](#summary-all-options)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Running debian servers

At the moment this describes tricks I had to do in debian 8 to debian 9 migrations related to linux kernel

# network interfaces

It's not clear for me why the change of interface names, but for some time I will maintain old style

add options:

    net.ifnames=0

    biosdevname=0

# I want to know what's going on

I always change default option of 'quiet' to 'verbose'. This makes boot a little bit slower, but if something is strange, I can see it in boot time easily (fast boot =>try to do a video and watch slowly)

# novnc proxmox resize issue

Got accostumated to the tiny proxmox novnc console in virtual machines. After some upgrade, it starts ok, but after boot line:

    fbcon: bochsdrmfb (fb0) is primary interface

it resizes. Grr!

You can avoid that adding to `/etc/default/grub` option `bochs_drm.fbdev=off` src https://unix.stackexchange.com/questions/346090/disable-framebuffer-in-qemu-guests

# summary: all options

GRUB_CMDLINE_LINUX_DEFAULT="net.ifnames=0 biosdevname=0 verbose bochs_drm.fbdev=off"
