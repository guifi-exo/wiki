# Configuració de túnels L2TP per routers OpenWRT/LEDE

Autor: Víctor Oncins 2017-11-12

El servei d'accés a Internet a través de l'eXO amb el protocol L2TP presenta certs avantatges. D'una banda millora els processos de gestió i control de la subscripció a Internet. De l'altra, simplifica la configuració dels routers residencials i permet integrar el suport de IPv4 i IPv6 a través d'una sola connexió. Els routers que suporten el sistema OpenWRT/LEDE permeten aquest tipus de connexió. Tanmateix hi ha routers amb firmwares propietaris que també el suporten. Si teniu un router residencial amb el firmware original, comproveu que el protocol L2TP està suportat.

El protocol L2TP encapsula una connexió de capa d'enllaç de tipus PPP. Ver obtenir més informació cliqueu el document de referència [LAA](https://github.com/guifi-exo/wiki/blob/master/howto/arquitectura-laa-acces-inet.md). La connexió PPP requereix un nom d'usuari i un password que serà proveït per l'associació eXO. Un cop disposem d'aquestes dades ja podem configurar el router OpenWRT. Els esquemes d'autenticació suportants pel conceptrador són PAP, CHAP i MSCHAP.

Aquesta és una guia tècnica per configurar aquest servei en routers residencials amb OpenWRT/LEDE. **Aquest document cobreix les versions estables d'OpenWRT 15.05.1 (Chaos Calmer) i LEDE 17.01.4 (Reboot).**

Podem trobar les imatges pre-compilades al dipòsit del projecte [OpenWRT](https://downloads.openwrt.org/chaos_calmer/15.05.1/) o [LEDE](https://downloads.lede-project.org/releases/17.01.4/). Trieu l'arquitectura de hardware i el model de router i procediu a gravar el nou firmware seguint les recomanacions dels webs dels respectius projectes.

## Instal·lació dels paquets necessaris

Suposem que tenim un router amb un firmware OpenWRT amb les configuracions per defecte. Un cop el tinguem a punt, connecteu el port WAN a una connexió a Internet. Si els valors de la configuració són els per defecte, hi haurà un client DHCP activat. Entrem al web de configuració http://192.168.1.1/. Entrem a la part *System > Software*. Cliquem *Update lists* i actualitzem la llista de dipòsits.

Cerquem el paquet *xl2tpd* i l'instal·lem. De manera opcional podem instal·lar d'altres com ara el *ip* o el *tcpdump* que poden ser útils en una fase posterior de depuració de problemes. Alternativament podem instal·lar tots els paquets de cop per línia de comandes:

```
root@OpenWrt:~# opkg update
root@OpenWrt:~# opkg install xl2tpd ip tcpdump
```

*Cal tenir en compte que no es recomana fer ús de dispositius de 4M de flash i 32M de RAM o menys.*

## Configuració de la connexió a Guifi.net

Cal tenir clar quina és la IP i rang (màscara) del node comunitari, típicament situat al terrat. Consulteu la pàgina web de Guifi.net o bé accediu directament al node. Normalment la IP té el format `10.a.b.c/27`. Reservem una nova IP dins d'aquest rang per router residencial, per exemple la `10.a.b.c+1/27`.

Anem a la part *Interfaces* i editem la WAN. Triem en el desplegable *Static address* i cliquem *Switch protocol*. Emplenem els camps amb aquests valors:

```
IPv4 address = 10.a.b.c+1
IPv4 netmask = 255.255.255.224
IPv4 gateway = 10.a.b.c
```

A l'apartat *Firewall Settings*, vinculem la interfície de xarxa a la zona WAN del firewall. Això impedirà l'accés de les connexions entrants al router residencial. Apliquem i desem canvis. Connectem el port que correspongui a la interfície WAN al cable del node comunitari o a l'equipment de xarxa que hi permeti l'accés. Assegurem-nos que teniu accés al concentrador de túnels de l'eXO:

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

Ens situem a la part de *Interfaces* i afegim una nova interfície clicant el botó *Add interface*. L'anomenem `exo`. Triem com a protocol de la nova interfície el L2TP. No hi vinculem cap interfície física. Apliquem els canvis i apareixeran els camps que caldrà emplenar:

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

**Si som en una xarxa de tipus mesh, cal que `Overrride MTU = 1420`, en cas contrari `Override MTU = 1436`.** Situem la nova interfície a la zona WAN del firewall a la part *Firewall Settings*. Apliquem i desem canvis.

## Configuració de la connexió d'accés a Internet per IPv6

L'eXO també proveeix d'accés a Internet per IPv6. Per activar-ho caldrà editar la interfície WAN6. Anem a *Physical Settings* i activem la següent opció tot emplenant el camp de text amb el valor `@exo`

- [X] Custom interface {@exo}

Apliqueu i deseu canvis. Per tal de fer efectiva la delegació del prefixe IPv6 provinent del concentrador, caldrà editar la interfície BR-LAN i modificar el camp següent:

```
IPv6 assigment length = 64
```
Deseu, apliqueu canvis i reinicieu el router. Un cop recuperat, ja hauríeu d'accepdir a Internet per IPv4 i IPv6.

## Resolució del bug de *redial* de L2TP

Les versions considerades d'OpenWRT i LEDE fan servir el mateix [paquet](https://github.com/openwrt/packages/tree/master/net/xl2tpd), que permet integrar la configuració del daemon `xl2tpd` en l'entorn UCI/LuCI. Tanmateix no permet activar la funció de *redial* del daemon *xl2tpd*, és a dir, quan es perd la comunicació i el túnel s'abaixa, aquest no es torna a recuperar automàticament, encara que la connextivitat amb el concentrador es reestableixi.

Per resoldre aquest problema i mentre els mantenidors oficials del paquet no ho solucionen, proposem el següent:

1. Baixeu-vos l'arxiu [l2tp.sh](https://github.com/guifi-exo/wiki/blob/master/howto/code/l2tp.sh), tot clicant l'opció *raw*.
2. Des del vostre PC executeu `scp l2tp.sh root@192.168.1.1:/lib/netifd/proto/l2tp.sh`
3. Inicieu de nou una sessió ssh amb el router i afegiu les línies que faltin respecte la següent secció de configuració de l'arxiu `/etc/config/network`:

```
config interface 'exo'
        option proto 'l2tp'
        option server '10.38.140.225'
        option username '<el-vostre-usuari>'
        option password '<el-vostre-password>'
        option ipv6 '1'
        option redial '1'
        option redial_timeout '15'
        option keepalive '30,10'
```

Un cop desats els canvis, reinicieu el router i ja tindrem la funció de reestabliment habilitada. El camp `redial` habilita (`1`) o deshabilita (`0`) la funció de reestabliment del túnel després del temps (en segons) especifiat en el camp `redial_timeout`. El valor `keepalive` configura el ritme de comprovacions de la salut del túnel. En aquest cas `30,10` vol dir que cada 10 segons envia un missatge de *keepalive*. En cas que després de 30 segons no es rebi cap resposta, es considera que el túnel està caigut i `xl2tpd` el donarà de baixa, tot activant la funció *redial*.
