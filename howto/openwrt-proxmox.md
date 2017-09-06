Written 2017-09-06

OpenWrt provides an image to "use existing disk". To do this is in proxmox is [a little bit tricky](https://forum.proxmox.com/threads/adding-an-existing-virtual-disk-image.7614/)

generic reference: https://wiki.openwrt.org/doc/howto/qemu

# Install

enter proxmox server by web, create virtual machine without media (DVD) and specific `VMID` I will assume VMID=200, and a disk of 60 MB

now enter via ssh

```
wget https://downloads.openwrt.org/chaos_calmer/15.05/x86/64/openwrt-15.05-x86-64-combined-ext4.img.gz
gunzip openwrt-15.05-x86-64-combined-ext4.img.gz
mv openwrt-15.05-x86-64-combined-ext4.img openwrt-15.05-x86-64-combined-ext4.raw
# raw works, but we will convert to qcow2 (because it has extra features) -> src https://docs.openstack.org/image-guide/convert-images.html
qemu-img convert -f raw -O qcow2 openwrt-15.05-x86-64-combined-ext4.raw openwrt-15.05-x86-64-combined-ext4.qcow2
cp openwrt-15.05-x86-64-combined-ext4.qcow2 vm-1002-disk1.qcow2
```

config file `/etc/pve/qemu-server/200.conf` should look like something like (here I did not include any network interface):

```
balloon: 0
bootdisk: virtio0
cores: 1
cpu: host
memory: 2048
name: openwrt
numa: 0
ostype: l26
scsihw: virtio-scsi-pci
smbios1: uuid=5fd0912e-7c0d-4bc0-8c63-642b376e2a43
sockets: 1
virtio0: local2:200/vm-200-disk-1.qcow2,size=60M
```
