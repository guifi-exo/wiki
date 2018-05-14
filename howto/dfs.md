DFS for 802.11s works when you set up encryption in the network (because this is the way where wpa-supplicant starts, and because DFS works through wpa-supplicant)

wpa-supplicant takes 1 minute scanning to get a free channel before it takes up

~~right now you cannot use mesh and access point in the same radio~~ Daniel fixed it (or is in its way)

"noscan" option in `/etc/config/wireless` allows you to use channels that are being used in the "secondary part" of a 40 MHz channel

next commands play with dfs and wifi driver:

    cd /sys/kernel/debug/ieee80211/phy0/ath9k

`chanbw` part allows you to subdivide the bandwidth of the channel to 5 MHz, this way, energy gets more concentrated. "this is how you can reach 100 km". TODO review how to use it (probably reading the linux kernel source code)

simulate radar:

    echo 1 > dfs_simulate_radar

`cat dfs_stats` get stats of DFS

Good practice: in tall places expect DFS, in short places don't expect DFS
