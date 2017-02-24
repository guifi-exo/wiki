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
