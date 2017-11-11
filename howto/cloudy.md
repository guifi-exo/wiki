# apply grub config

Dear Cloudy users,

A few of the people who participated in the Cloudy Minix Z64 devices giveaway some months ago reported that the eMMC flash storage of the devices was failing, as the operating system informed that it was unable to read or write to certain memory addresses, which lead to the device becoming unresponsive. We could detect the same issue, but we were unable to determine a pattern that caused the memory to fail: the error would appear on a different block every time, without any specific action that triggered it.

After performing many test, we found out that the eMMC errors were more prone to appear when using newer Linux kernels (e.g. 4.3), like the ones shipped in the Debian Jessie backports repositories. Recently, when searching for related information, we found a web page [1] were this issue was also discussed, and a workaround was suggested. To the best of our knowledge, therefore, the eMMC errors are not caused by a defective memory component, but by a combination of the Intel CPU C-states [2], the eMMC and the Linux kernel functionalities.

During the last days we have been performing several tests with a few Minix Z64. We have seen that (as it is suggested here [1]) disabling certain CPU C-states avoids the eMMC errors reported. To achieve it, you have to do the following:

1) Edit the file "/etc/default/grub" and add the string "intel_idle.max_cstate=2" to the "GRUB_CMDLINE_LINUX_DEFAULT" line:
   GRUB_CMDLINE_LINUX_DEFAULT="intel_idle.max_cstate=2 quiet"
2) Update Grub:
   # update-grub (as root)
   $ sudo update-grub (as a regular user)
3) Reboot

These steps ensure that the CPU does not enter the low power consumption C-states that cause the malfunctioning of the eMMC storage. This comes, however, at the expense of a slight increase in power consumption.

We encourage all of you who have a Minix Z64 to perform the steps above.

Kind regards,
