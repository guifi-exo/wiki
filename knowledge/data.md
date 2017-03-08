# ISO image

per defecte el sistema escriu en blocs de 64

```
cp /path/to/iso /dev/sdc
sync
```

Però una memòria flash està estructurada per borrar blocs de 1024k, és millor si adaptem a aquest tamany l'escriptura

`dd if=/path/to/iso of=/dev/sdX bs=1024k conv=fsync`

# Services

## nextcloud

src https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-nextcloud-on-ubuntu-16-04

# Disks

## SSD

SSD: recordeu que tenen una vida limitada degut a la durada de les celes MLC, si escriviu moltes vegades el disc peta per desgast i la garantia no ho cobreix

Els SSD desktop tenen 3 anys de garantia si són de qualitat i permetent 0.1 (<0.3) full disk write per day

Això vol dir que un discs desktop de 500GB permet escriure fins a 500GBx0.1=50GB per dia durant 3 anys= 53TiB

Un disk SSD Enterprise read intensive permet 0.3 Full Disk Write per Day durant 5 anys, en aquest cas 500GB*0.3=150GB per dia durant 5 anys= 267TiB

Hi han discs Enterprise que els hi diuen Mix Load amb 3x Full Disk Writes per Day i els que reben la denominació Write Intensive que suporten 10x ( o més) Full Disk Write per Day, en els dos casos durant 5 anys de garantia

Si només és per el SO amb els desktop de 0.1 FDWD durant 3 anys és prou correcte però si hi han BBDD millor un nivell Enterprise...

el important per la durada desl dispositius és la temperatura de treball i les variacions d'aquesta

les variacions afecten més als dispositius electromecanics degut a les dilatacions

però en tots els casos la vida mitja estimada s'escurça a la meitat per cada 10° d'increment de temperatura

això és el MTBF (Mean Time Before Failure) que és completament estadístic i extrapolat i cada fabricant ho fà com li sembla

el SSD d'Intel tenen 5 anys de garantia i 2.000.000 hores de MTBF

# Filesystems

XFS: XFS is a File system which is designed for high performance ,scalability and Capacity point of view. It is generally used where large amount data to be stored / used on the File system. Some of the awesome freeze features of xfs are xfs_freeze, snapshot, xfs_unfreeze. One of the limitation of XFS is that we can not shrink or reduce this file system. src: http://www.linuxtechi.com/create-extend-xfs-filesystem-on-lvm/

LVM: With LVM we can snapshot our volumes

# Snapshots

An sparse file is a simple version of thin provisioning. Note: this files only can grow.

thin provisioning:
- copy on write
- data is hardlinked in another place, when data start changing it starts to differs from the two places. That way, we are doing a natural snapshot
- some metadata stuff

qcow:
- thin provisioning: només fas servir espai dels blocs que estan plens. 
- snapshot:
- allows compression in the [backup](https://pve.proxmox.com/wiki/VMA#VMA_backup_format)

# Experimental

It would be interesting to evaluate Brtfs as a solution for snapshots and/or as a backup solution

https://btrfs.wiki.kernel.org/index.php/Incremental_Backup
