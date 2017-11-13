# Servei d'accés a Internet per L2TP Aggregation Architecture (LAA)

Autor: Víctor Oncins 2017-10-05

Com a novetat es planteja un nou router d'accés per usuaris específics (ITConic-LNS) que permeti l'accés directe a Internet a través d'un procés d'AAA. Aquest nou paradigma d'accés permetria:

* Control centralitzat de l'accés
* Autenticació de la subscripció (local, PAM, RADIUS, ...)
* Assignació dinàmica d'adreces públiques o de Guifi.net
* Establiment sota arquitectura client-servidor, cosa que elimina els possible problemes de NAT i DNS dinàmics que es donen amb els túnels estàtics GRE/IPIP

Una solució coneguda pels ISPs per aquest tipus d'accés és l'arquitectura L2TP Aggregation Architecture o [LAA](https://www.broadband-forum.org/technical/download/TR-025.pdf). Aquesta solució es basa en una xarxa de commutació de paquets (L3 PSN) que en el nostre cas pot ser Guifi.net o les xarxes amb peering de la FXOLN. L'escenari contemplat seria el següent:

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

Els Border Network Gateway (BNG) fan servir les funcions de LAC i LNS de L2TP però redirigint els paquets PPPoE cap el LNS. Aquest paradigma de connexió té cert avantatges:

 * Permet connectar múltiples CPE de usuari situats en el mateix emplaçament, és a dir emprant els mateixos punts extrems L2TP
 * PPPoE és un protocol implementat per molts fabricants, distribucions de routing i dispositius personals

Tanmateix la implementació de la LAA requereix de més anàlisi. Tot i que les distribucions basades en Linux (VyOS i OpenWRT) suporten l'establiment de túnels L2TP per PPP, la funcionalitat prevista requereix una implementació que permeti que els paquets PPPoE generats pel CPE d'usuari s'encapsulin dins un túnel L2TP. És a dir, que elimini les capceleres Ethernet i el procés de AAA i IPCP es faci directament entre el CPE i ITConic (LNS). Per la funció de LAC forwarder només hem trobat una distribució de codi obert que és [BSDRP](https://bsdrp.net/) (FreeBSD). El següent quadre resumeix les funcions suportades per cada implementació:


| Distribució     | L2TP LAC forwarder |L2TP LAC no-IPsec |L2TP LNS no-IPsec | 
| ----------------| ------------------ |----------------- |------------------|
| RouterOS 6.38.X | NO                 | SI               | SI               |
| VyOS 1.1.7      | NO                 | NO               | NO               |
| BSDRP 11.1      | SI                 | SI               | SI               |
| OpenWRT CC      | NO                 | SI               | SI               |
