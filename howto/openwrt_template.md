# node habitual

nota: utilitzar trunk per tenir nova versió de bmx6 (amb la vella funciona)

    bmx6-json bmx6-sms bmx6-uci-config bmx6-table luci luci-ssl

opcional

    luci-app-bmx6 tcpdump-mini

# node frontera

nota: utilitzar trunk per tenir nova versió de bird i bmx6 (amb la vella luci-app-bird4 no funciona)

afegir:

    bird4 bird4-uci birdc4 luci-app-bird4

és a dir:

    bmx6-json bmx6-sms bmx6-uci-config bmx6-table luci luci-ssl bird4 bird4-uci birdc4 luci-app-bird4
