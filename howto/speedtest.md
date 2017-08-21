Speedtest

# speedtest.exo.cat

basat en: https://github.com/adolfintel/speedtest

directori: /var/www/speedtest/

html: index.html

El backend es speedtest.js. garpage.php l'unic que fa es generar dades per descarregar

- speedtest.net dóna més (?). vol dir que no és precís?

- TODO: gràfics de estadística

# iperf

ja s'utilitza iperf a vegades, però s'estudia deixar-ho permanent

- cal evitar que es puguin fer peticions des d'internet (només des de dins de guifi) -> iptables source address guifi i obrir tcp i udp al port 5001

# speedtest en nodejs

github: https://github.com/soterinsights/speedtest

speedtest.js: 120 línies (fàcil!)
actualment funciona però conté massa informació, hauria de ser més fàcil
