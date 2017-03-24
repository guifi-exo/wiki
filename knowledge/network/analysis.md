Software running:

- Network troubleshooting
- Analysis
- Software and communications protocol development
- Education

**wireshark** is a GUI program that you will find for all platforms: GNU/Linux, Mac and Windows.

**tcpdump** is a CLI program that you will find in LEDE and OpenWrt. This program can show you on stdout what's going on, or save a pcap file to analyze with wireshark.

To visualize wireshark everywhere you can use this one-liner command (explanation below):

`ssh $1 "tcpdump -U -s0 -w - not port 22 || sudo tcpdump -U -s0 -w - not port 22" | wireshark -k -i -`

$1 could be:
- an argument if you do this a bash script
- a `~/.ssh/config` host
- a destination `root@10.x.x.x`

sometimes you can run tcpdump inmediately (you are root), sometimes you need sudo (is the case for ubiquiti edgemax), if you need [passwordless sudo for a specific command](http://askubuntu.com/questions/159007/how-do-i-run-specific-sudo-commands-without-a-password) you can do it. Sometimes, sometimes: that is why is there the binary operator OR `||`

tcpdump listen all interfaces and send the data through ssh to our local computer and wireshark interpret it

you have to execute this command each time you want a new capture

in my case, I use it as function _aliased_ in `~/.bash_aliases`:

`alias sws='function _swireshark() { ssh $1 "tcpdump -U -s0 -w - not port 22 || sudo tcpdump -U -s0 -w - not port 22" | wireshark -k -i - }; _swireshark'`

this way, each time I do `sws myHost` (taken from `~/.ssh/config`, starts the capture. sws for me means: Ssh WireShark. Seems that is available and no software is using it.
