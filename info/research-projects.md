Research projects interesting for eXO, guifi that could be done by its community, external/conctracted professionals or as academia work

important notes: 

- this document is a draft
- information here could be outdated

# Decentralized DNS

A (simple?) decentralized DNS solutions that fits in embedded devices (lightweight) to have FQDN services with letsencrypt certificates inside the community network. Interesting additional features: revision control/snapshots and trusting framework to improve control of the registers and avoid attacks.

# Solar node

OpenMPPT tracker, [presentation](https://github.com/elektra42/freifunk-open-mppt/blob/master/Freifunk-Open-MPPT-English.pdf)

18 V SOLAR PANEL 50 WATT [1](https://www.amazon.de/enjoysolar%C2%AE-Polykristallin-Solarmodul-Solarpanel-Wohnmobil/dp/B076B3Z48G?SubscriptionId=AKIAILSHYYTFIVPWUY6Q&tag=duckduckgo-ffsb-de-21&linkCode=xm2&camp=2025&creative=165953&creativeASIN=B076B3Z48G)

battery example [1](https://www.reichelt.com/de/en/Lead-Acid-Batteries-Kung-Long/WP-18-12/3/index.html?ACTION=3&LA=2&ARTICLE=44425&GROUPID=4232&artnr=WP+18-12&trstct=pol_14&SID=94WvXc46wQATMAAHIShQMfc78bb6a5f6916d42ae1066844b9e377) [2](https://www.amazon.de/LONG-Bleiakku-WP18-12I-12V-18Ah/dp/B0746J9F6Z?SubscriptionId=AKIAILSHYYTFIVPWUY6Q&tag=duckduckgo-ffhp-de-21&linkCode=xm2&camp=2025&creative=165953&creativeASIN=B0746J9F6Z)

Antena of 3W: tplink 841, tplink 510 (TODO: requires compatibility with latest version)

Translation needed from German to English -> https://elektrad.info/download/Freifunk-OpenMPPT-Handbuch-26-August-2017.pdf

Origin: Elektra

# Secure mesh

Configuration and documentation about a network that is very secure and DFS ready

Good practice: in tall places expect DFS, in short places don't expect DFS

- Encrypted links
- bmx7 with its "trusted routing"

Origin: Daniel Gölle

# Peerstreamer

- Clustering in the serverside
- How to put the streaming in RTP, how to play it?
- Get capture screen working, use cases:
    - get scream of presenter in a conference through web application (no specific cable: VGA, HDMI, etc.)
    - twitch.tv style service in a decentralized manner

# Retroshare

Discard nextcloud to upload massive content and other similar services. This puts risks on system administrators: it is better an encrypted P2P file sharing system

Origin: Gioacchino Mazzurco

# Open source TDMA

Wifi vs TDMA => TDMA wins

It is needed a solution that competes with privative TDMA solutions like (ubiquiti) and (mikrotik) technologies

Meanwhile document how to jam frequency (oh sorry no, a secret link protocol that takes all spectrum for him) during hard negotiations 

# Open source implementation of 802.1aq

https://en.wikipedia.org/wiki/IEEE_802.1aq

The "new" ethernet standard works mostly as MPLS (useful for multitenant network) but it is backward compatible with the old ethernet protocols which reduce its overall complexity. At the moment is not available in Linux platforms

# Improve wireguard

Wireguard is not prepared yet for community netowrks. It uses a global clock and requires routers to synchronize NTP before they connection (chicken-egg problem)

# Application to promote socialization between community network members

Inspired by [tubechat](http://tube.chat/) presentation in battlemesh, an application that improves the relation and interaction between the people involved in the community network would be an interesting application. Creative ways so they discover them on the same network they are; and ways to keep the contact.

# raspberry pi + spi interface

Document the way to flash rom of bricked routers using SPI interface connector through the GPIO interface of raspberry pi and `flashrom` program


# Community network

## (1) Network descriptor (proof of concept)

This section assumes that autoconfiguration methodologies (libremesh, gluon) or a specific centralized technology (guifi.net) does not help to:

- get more people involved
- complexity equal to simple
- maintenance

The proposed approach is to get consensus on the full specification / description of a network. [Netjson](https://netjson.org) is a good try, but only describes specific nodes and its links. It is required the data of a zone as seen in guifi webpage

The proposition is to write a proof of concept tool in python where in a git repository:

- a zone is a directory
- `.zone` is a file that describes the zone: IP delegation to this node, who is admin or responsible, etc.
- a node is a file described in netjson format

note: when this description grows will go to a git repo itself

Inspiration:

- password-store.org
- netjson.org
- guifi webpage & cnml
- yanosz pointed me to:
    - python script to run VPNs https://github.com/freifunk/icvpn
    - data: https://github.com/freifunk/icvpn-meta


Origin: guifipedro

## (2 and 3) Template-based firmware

Get one firmware for a specific device in a static oriented way (no autoconfiguration or the need of firmwares like libremesh or gluon)

- (2) Compilation through specific profile (device) and the packages required by its role
- (3) Template configuration: /etc/config

quality measure: mark specific commit. fork relevant git repositories? routing?

Inspiration: Yanosz

Origin: guifilab / barcelona community

# online judge programming challenge resource

Educational and brain-fitness project to improve programming and developer skills for community network folks
