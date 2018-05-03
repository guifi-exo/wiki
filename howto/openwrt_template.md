cause: use ansible to template configuration of well-known devices

status: work in progress

# normal node

nota: utilitzar trunk per tenir nova versió de bmx6 (amb la vella funciona)

    bmx6-json bmx6-sms bmx6-uci-config bmx6-table luci luci-ssl

opcional

    luci-app-bmx6 tcpdump-mini

in flavors.conf (lime-sdk)

    normal_node="bmx6-json bmx6-sms bmx6-uci-config bmx6-table luci luci-ssl"

# border node

nota: utilitzar trunk per tenir nova versió de bird i bmx6 (amb la vella luci-app-bird4 no funciona)

afegir al node habitual lo que el fa que sigui frontera:

    bird4 bird4-uci birdc4 luci-app-bird4

és a dir:

    bmx6-json bmx6-sms bmx6-uci-config bmx6-table luci luci-ssl bird4 bird4-uci birdc4 luci-app-bird4 luci-app-bmx6 tcpdump-mini

in flavors.conf (lime-sdk)

    border_node="bmx6-json bmx6-sms bmx6-uci-config bmx6-table luci luci-ssl bird4 bird4-uci birdc4 luci-app-bird4 luci-app-bmx6 tcpdump-mini"

# how to use a particular bmx6 commit

feeds/routing/bmx6/Makefile

change variable `PKG_REV` as desired. this is how it looks the file https://github.com/bmx-routing/openwrt-routing-packages/blob/master/bmx6/Makefile

notes:

- qmp 3.2.1: `revision=2a87b770d3f9c254e3927dc159e2f425f2e0e83a`

# extra sources

- https://openwrt.org/docs/guide-developer/build-system/use-buildsystem
- https://openwrt.org/docs/guide-developer/start
- https://openwrt.org/docs/guide-developer/build-system/start
