# Configuració de túnels L2TP per routers OpenWRT/LEDE

Autor: Víctor Oncins 2017-11-12

El servei d'accés a Internet a través de l'eXO amb el protocol L2TP presenta certs avantatges. D'una banda millora els processos de gestió i control de la subscripció a Internet. De l'altra simplifica la configuració dels routers residencials i permet integrar el suport de IPv4 i IPv6 a través d'una sola connexió. Els routers que suporten el sistema OpenWRT/LEDE permeten aquest tipus de connexió. Tanmateix hi ha routers amb firmwares propietaris que també el suporten. Si teniu un router residencial amb el firmware original, comproveu que el protocol L2TP està suportat.

El protocol L2TP encapsula una connexió de capa d'enllaç de tipus PPP. La connexió PPP requereix un nom d'usuari i un password que serà proveït per l'associació eXO. Un cop disposem d'aquestes dades ja podem configurar el router OpenWRT.

*Aquest document cobreix les versions estables d'OpenWRT 15.05.1 (Chaos Calmer) i LEDE 17.01.4 (Reboot).*

## Instal·lació dels paquets necessaris

Suposem que tenim un router amb un firmware OpenWRT amb les configuracions per defecte. Podem trobar les imatges pre-compilades al dipòsit del projecte [OpenWRT](https://downloads.openwrt.org/chaos_calmer/15.05.1/) o [LEDE](https://downloads.lede-project.org/releases/17.01.4/). Trieu l'arquitectura de hardware i el model de router i procediu a gravar el nou firmware. Un cop el tinguem a punt, connecteu la porta WAN a una connexió a Internet. Si els valors de la configuració són per defecte, hi haurà un client DHCP activat. Entrem al web de configuració http://192.168.1.1/. Entrem a la part *System > Software*. Cliquem *Update lists* i actualitzem la llista de dipòsits.

Cerquem el paquet *xl2tpd* i l'instal·lem. De manera opcional podem instal·lar d'altres com ara el *ip* o el *tcpdump* que poden ser útils en una fase posterior de depuració de problemes. Alternativament podem instal·lar els paquets per línia de comandes:

```
root@OpenWrt:~# opkg update
root@OpenWrt:~# opkg install xl2tpd ip tcpdump
```

## Configuració de la connexió a Guifi.net

Cal tenir clar quina és la IP i rang (màscara) del node comunitari, típicament situat al terrat. Consulteu la pàgina web de Guifi.net o bé accediu directament al node. Normalment la IP té el format `10.a.b.c/27`. Reservem una nova IP dins d'aquest rang per router residencial, per exemple la `10.a.b.c+1/27`.

Anem a la part *Interfaces* i editem la WAN. Triem en el desplegable *Static address* i cliquem *Switch protocol*. Emplenem els camps amb aquests valors:

```
IPv4 address = 10.a.b.c+1
IPv4 netmask = 255.255.255.224
IPv4 gateway = 10.a.b.c
```

A l'apartat *Firewall Settings*, vinculem la interfície de xarxa a la zona WAN del firewall. Això impedirà l'accés de les connexions entrants al router residencial. Apliquem i desem canvis. Connectem el port que correspongui a la interfície WAN al cable del node comunitari o a l'equipment de xarxa que hi permeti l'accés. Assegurem-nos que teniu accés al concentrador de connexión de l'eXO:

```
root@OpenWrt:~# ping 10.38.140.225
PING 10.38.140.225 (10.38.140.225): 56 data bytes
64 bytes from 10.38.140.225: seq=0 ttl=61 time=6.780 ms
64 bytes from 10.38.140.225: seq=1 ttl=61 time=4.980 ms
^C
--- 10.38.140.225 ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max = 4.980/5.880/6.780 ms
```

## Configuració de la connexió L2TP d'accés a Internet IPv4

Ens situem a la part de Interface i afegin una nova interfície clicant el botó *Add interface*. L'anomenem `exo`. Triem com a protocol de la nova interfície el *L2TP*. No hi vinculem cap interfície física. Apliquem els canvi i apareixeran els camps que caldrà emplenar:

```
L2TP Server = 10.38.140.225
PAP/CHAP username = <nom d'usuari proveït per eXO>
PAP/CHAP password = <password proveït per eXO>
```
A la secció *Advanced Settings*, marquem els punts següents:

- [X] Bring up on boot
- [x] Use builtin IPv6-management
- [x] Use default gateway
- [x] Use DNS servers advertised by peer (Opcional)

Si som en una xarxa de tipus mesh el camp `Overrride MTU = 1420` en cas contrari `Override MTU = 1456`. Situem la nova interfície a la zona WAN del firewall a la part *Firewall Settings*. Apliquem i desem canvis.


