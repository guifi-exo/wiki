# Configuració de túnels L2TP per routers OpenWER/LEDE

Autor: Víctor Oncins 2017-11-12

El servei d'accés a Internet a través de l'eXO amb el protocol L2TP presenta certs avantatges. D'una banda millora els processos de gestió i control de la subscripció a Internet. De l'altra simplifica la configuració dels routers residencials i permet integrar el suport de IPv4 i IPv6 a través d'una sola connexió. Els routers que suporten el sistema OpenWRT/LEDE permeten aquest tipus de connexió. Tanmateix hi ha routers amb firmwares propietaris que també el suporten. Si teniu un router residencial amb el firmware original, comproveu que el protocol L2TP està suportat.

El protocol L2TP encapsula una connexió de capa d'enllaç de tipus PPP. La connexió PPP requereix un nom d'usuari i un password que serà proveït per l'associació eXO. Un cop disposem d'aquestes dades ja podem configurar el router OpenWRT.

*Aquest document cobreix les versions estables d'OpenWRT 15.05.1 (Chaos Calmer) i LEDE 17.01.4 (Reboot).*

## Instal·lació dels paquets necessaris

Suposem que tenim un router amb un firmware OpenWRT amb les configuracions per defecte. Podem trobar les imatges pre-compilades al dipòsit del projecte [OpenWRT](https://downloads.openwrt.org/chaos_calmer/15.05.1/) o [LEDE](https://downloads.lede-project.org/releases/17.01.4/). Trieu l'arquitectura de hardware i el model de router i procediu a gravar el nou firmware. Un cop el tinguem a punt, connecteu la porta WAN a una connexió a Internet. Si els valors de la configuració són per defecte, hi haurà un client DHCP activat. Entrem al web de configuració http://192.168.1.1/. Entrem a la part *System > Software*. Cliquem *Update lists* i actualitzem la llista de dipòsits.

Cerquem el paquet *xl2tpd* i l'instal·lem. De manera opcional podem instal·lar d'altres com ara el *ip* o el *tcpdump*.


```
               SN/Client                  L3 PSN                PoP-IX  

+-----------+           +-----------+    +------+    +-------+          +------+
|           |           |           |    |      |    |       |          |      |
| PC1/ CPE1 +-----------+           +<-----L2TP----->+       |          |      |
|           |<==PPPoE==>*<=========>*<====PPP+AAA===>|       |          |  IX  |
+-----------+           |           |    |      |    |       +--VLAN95--+      +->FXOLN
+-----------+           |    LAC    |    |      |    |       |          |      |
|           |           |           |    |      |    |       |          |      |
| PC2/ CPE2 +-----------+           |    |      |    |       |          |      |
|           |<==PPPoE==>*<=========>*<====PPP+AAA===>+  LNS  |          |      |
+-----------+           +-----------+    |      |    |       |          |      |
                                         |      |    |       |          |      |
  +---------+           +-----------+    |      |    |       |          +------+
  |         |           |    LAC    |    |      |    |       |
  |   PC    +-----------+   usuari  +<-----L2TP----->+       |          +------+
  |         |           |    NAT    |<====PPP+AAA===>|       |<==AAA===>|RADIUS|
  +---------+           +-----------+    +------+    +-------+          +------+
```


| Distribució     | L2TP LAC forwarder |L2TP LAC no-IPsec |L2TP LNS no-IPsec | 
| ----------------| ------------------ |----------------- |------------------|
| RouterOS 6.38.X | NO                 | SI               | SI               |
| VyOS 1.1.7      | NO                 | NO               | NO               |
| BSDRP 11.1      | SI                 | SI               | SI               |
| OpenWRT CC      | NO                 | SI               | SI               |
