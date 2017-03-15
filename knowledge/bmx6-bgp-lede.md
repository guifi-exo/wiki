<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [Integració entre BMX6 i BGP en dispositius basats en LEDE](#integraci%C3%B3-entre-bmx6-i-bgp-en-dispositius-basats-en-lede)
  - [Descripció de l'escenari i objectius](#descripci%C3%B3-de-lescenari-i-objectius)
  - [Estratègia general](#estrat%C3%A8gia-general)
  - [Descripció de les plataformes de proves](#descripci%C3%B3-de-les-plataformes-de-proves)
    - [Compilar LEDE](#compilar-lede)
  - [Diagrama funcional dels daemons de routing Bird i BMX6](#diagrama-funcional-dels-daemons-de-routing-bird-i-bmx6)
    - [Detall de les configuracions finals](#detall-de-les-configuracions-finals)
  - [Proves i conclusions](#proves-i-conclusions)
    - [Prova amb llista completa de prefixos](#prova-amb-llista-completa-de-prefixos)
    - [Prova amb llista parcial de prefixos](#prova-amb-llista-parcial-de-prefixos)
  - [001-filters_fix_new_protocols.patch](#001-filters_fix_new_protocolspatch)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Integració entre BMX6 i BGP en dispositius basats en LEDE

Autor: Víctor

Les xarxes basades en el protocol [BMX6](http://bmx6.net/projects/bmx6) o mesh en el sentit més ampli, constitueixen part de la xarxa guifi.net des de fa alguns anys. BMX6 és un protocol de routing dinàmic de capa 3 de tipus vector de distància. BMX6 permet establir un domini de routing intern, és a dir, els nodes que el conformen són capaços d'anunciar i calcular la distància a certa destinació, i finalment triar el veí més adient. Fóra d'aquests dominis BMX6 l'anunci de prefixes i càlcul de rutes es
fa amb protocols diferents, ja sigui OSPF o bé BGP.

Un dels principals problemes que hi ha és la correcte integració entre una xarxa basada en BMX6 i els nodes frontera BGP de tal manera que:

- Els prefixes de xarxa del domini BMX6 s'anunciïn cap els peers BGP
- Els prefixes de xarxa provinents dels peers BGP s'anunciïn dins el domini BMX6
- Que dos o més routers frontera BGP anunciïn els prefixes externs al domini i que aquest permeti el trànsit

En una primera fase els dos primers punts s'han implementat amb èxit a les xarxes de Sant Andreu, La Sagrera i P9SF. En aquests moments es troben sota el mateix domini de routing BMX6 a través d'enllaços metropolitans FTTH. El tercer punt és el que presenta més dificultats.

La única implementació de BMX6 no és inclosa en cap producte o firmware comercial. Les xarxes mesh implantades a Guifi.net fan servir [QMP](http://qmp.cat) com *third-part* firmware. Aquest firmware suporta el maquinari més emprat en aquestes xarxes, és a dir, Nanostation M5 de Ubiquiti Networks.

Tanmateix, els nodes que han de implementar les funcions de integració amb BGP requereixen de configuracions massa específiques que estan fóra de l'abast de QMP.

Hem abordat una solució al problema de la manera més general possible per tal que sigui reproduïble a d'altres xarxes. Passem doncs a descriure el plantejament de l'escenari i a avaluar-ne els resultats.

## Descripció de l'escenari i objectius

Considerem una xarxa basada en BMX6 com les desplegades actualment a Guifi.net a Barcelona. Quasi tots els nodes incorporen una o més interfícies WLAN a 5GHz 802.11n amb maquinari de baix cost, típicament Nanostation M5. En uns pocs emplaçaments es disposa de maquinari especialitzat en l'intercanvi de rutes i accés a Internet. Aquests emplaçaments compten (o poden comptar fàcilment) amb encaminadors amb **únicament interfícies Ethernet, amb força més recursos de CPU i memòria* que la resta de nodes WLAN.

Considerem que tenim dins d'una xarxa o domini BMX6 dos d'aquests encaminadors que anomenem *Nodes de intercanvi mesh (MXN)*. Aquests estan enllaçats d'una banda a un supernode veí de *infraesctructura (ISN)* i de l'altra a la resta de la xarxa BMX6 per interfícies Ethernet. Considerem també que els supernodes veïns implementen BGP i tenen números d'AS diferents.

Segons veiem a la següent figura, els nodes ISN1 i ISN2 estableixen les corresponents connexions BGP amb els MXN1 i MXN2. Donat que tenen números de AS diferents, apliquen la variant eBGP del protocol BGP. Com que estan connectats a través d'una mateixa interfície de xarxa, els prefixes anunciats des de ISNx i rebuts per ISNx es tradueixen en rutes de tipus *reachable* a les respectives taules del kernel. Tanmateix MXN1 i MXN2 en general no estan connectats directament. BMX6 no estableix túnels entre els nodes de manera permanent i completament bidireccionals, de manera que a efectes del daemon de routing BGP no es consideren directament connectats.

~~~ {}
   (E)                                                                   (F)
    |                                                                     |
+---+---+                                                             +---+---+
|  ISN1 |                                                             |  ISN2 |
|  AS1  |                                                             |  AS3  |
+---+---+                                                             +---+---+
    | ^                                                                  ^|
    | |(A)    +------+             +----+                +------+     (B)||
    | +------>| MXN1 |             |    |                | MXN2 |<-------+|
    +---------+ AS2  +-----\...\---+ MN +-----\....\-----+ AS2  +---------+
              |      |<------(C)-->|    |<------(D)----->|      |
              +------+             +----+                +------+
~~~

**Els objectius són:**

1. Permetre l'intercanvi dels prefixes de xarxa entre ISN1 i ISN2 de manera que un paquet provinent de (E) i de (F) arribi a la seva destinació a través del domini de routing BMX6
2. Anunciar els prefixes a tot el domini BMX6 provinents de ISN1 i ISN2
3. Anunciar els prefixes de les xarxes contingudes dins el domini cap a ISN1 i ISN2

## Estratègia general

Comencem discutint els anteriors punts (2) i (3). En el nostre escenari BMX6 fa les funcions de *Protocol d'Encaminament Intern (IGP)*. BMX6 calcula quin és el millor veí per assolir totes les destinacions (prefixes) anunciats per altres nodes (MN) que també implementen BMX6. En acabat, insereix a la taula de rutes la corresponent ruta cap aquella subxarxa. Per defecte aquesta taula és la *main* en sistemes Linux. D'altra banda BMX6 compta amb una extensió de programari (plugin Table) que permet anunciar automàticament els prefixes continguts a qualsevol taula de routing del sistema. Per tant, si usem una nova taula d'encaminament i fem que el daemon que implementa el protocol BGP insereixi les rutes anunciades pels peers BGP (A) i (B), podem satisfer l'objectiu 2. De manera inversa, el protocol BGP pot anunciar els prefixos que BMX6 ha inserit prèviament en forma de rutes a la taula *main* corresponents a subxarxes de dins el domini, satisfent l'objectiu 3.

Si un paquet cap a E arriba a ISN2, no té encara manera de saber que MXN2 pot encaminar-lo. Per resoldre aquest problema i per tant assolir l'objectiu 1, recorrem a l'establiment d'un peer BGP entre MXN1 i MXN2, és a dir, un BGP intern (iBGP). Amb una configuració adequada del daemon de BGP és possible transferir directament a rutes assolibles (*reachable*) els prefixes anunciats dins el peer iBGP. En aquest cas, ISN2 si que sabrà on enviar el paquet cap a E: el seu veí MXN2. Aquest encaminador per la seva banda ja ha rebut l'anunci per BMX6 del prefix de E i sap que MXN1 pot encaminar-lo.

**Aquesta solució implica que els anuncis enviats per iBGP i per BMX6 siguin coherents, és a dir, que mai s'anunciï un prefix pels peers eBGP que no pugui ser encaminat per BMX6.**


## Descripció de les plataformes de proves

Tot i que en en les xarxes en producció els nodes MN implementen [QMP](http://qmp.cat) sobre maquinari típicament de Ubiquiti Networks, hem trobat dificultats en usar aquest mateix firmware en els nodes MXN basats en configuracions avançades. [QMP](http://qmp.cat) permet la incorporació senzilla de nodes MN i per això implementa processos automàtics d'autoconfiguració basats en hipòtesis que no apliquen en els MXN. Hem preferit una alternativa minimalista, és a dir, que només implementi el programari estrictament necessari sense automatismes i plantejaments de programació *a priori*.

Pels MXN hem compilat una imatge de [LEDE](https://www.lede-project.org/) amb els següents paquets:

1. luci
2. bmx6, bmx6-uci-config, bmx6-json, bmx6-table i bmx6-sms
3. bird4, birdc4, bird4-uci
4. luci-app-bmx6 i luci-app-bird4

De manera complementària hem incorporat els paquets i mòduls del kernel *gre* i *ipip* per tal de poder usar els túnels GRE/IPIP per establir enllaços per FTTH a d'altres MXN.

Hem optat per [Bird](http://bird.network.cz/) com a daemon de routing dinàmic BGP, tot i que implementa altres protocols. Aquest programari és força versàtil i relativament fàcil de configurar. Permet també implementar filtres força sofisticats gràcies a un llenguatge d'scripting força potent i suporta taules de routing múltiples de manera natural.

Pel que fa al maquinari hem triat plaques Alix 2D2/2D3 Geode x86.

### Compilar LEDE

Comencem per clonar el repositori *git* de LEDE. Donem per suposat que el nostre sistema de compilació compta amb els paquets necessaris per fer-ho. Consulteu requeriments [aquí](https://wiki.openwrt.org/doc/howto/buildroot.exigence).

~~~ {.bash}
git clone http://git.lede-project.org/source.git
~~~
això crearà el directori de treball *source*. Si estem interessats en configurar túnels GRE/IPIP amb extrems amb IPs dinàmiques, podeu instal·lar el paquet *dtun* que de moment no es troba en els repositoris oficials. En aquest cas editeu l'arxiu *feeds.conf.default* i afegiu la darrera línia:

~~~ {}
src-git dtun https://github.com/dyangol/dtun.git
~~~

Després hem de descarregar i instal·lar els *feeds* de tots els paquets de LEDE per tal de triar els que volem incloure en la imatge.

~~~ {.bash}
cd source
./scripts/feeds update -a
~~~

En el nostre cas hem obtingut les següents versions de cada paquet rellevant:

- bmx6: revisió [2a87b770d3f9c254e3927dc159e2f425f2e0e83a](https://github.com/axn/bmx6/tree/2a87b770d3f9c254e3927dc159e2f425f2e0e83a), versió r2015080701
- bird: versió 1.6.0
- bird4-openwrt: versió 0.2

El darrer paquet *bird4-openwrt* permet gestionar l'arxiu de configuració de Bird des de la interfície de gestió web. Aquesta extensió de LuCI per gestionar el daemon Bird, conté diversos *bugs* que hem hagut de resoldre. D'altra banda hem hagut d'ampliar el suport de determinats protocols que han estat necessaris per implementar la solució. En el moment d'escriure aquestes línies encara no s'ha aprovat el *pull request* en el repositori oficial. El patch `001-filters_fix_new_protocols.patch` es troba al final d'aquest document i cal incloure'l en un nou directori *feeds/routing/bird-openwrt/bird4-openwrt/patches/*. Quan es compili la imatge s'aplicarà el patch. Instal·lem els paquets en l'estructura d'arxius de LEDE:

~~~ {.bash}
./scripts/feeds install -a
~~~

Creem un nou arbre de directoris per tal d'incorporar les configuracions per defecte incloses en el moment de la compilació. En concret afegim l'arxiu *rt_tables* modificat per tal de crear la taula 251 sota l'àlies *ebgp*:

~~~ {.bash}
mkdir -p files/etc/iproute2
~~~

Aquest arxiu ha de tenir aquesta forma:

~~~ {}
#
# reserved values
#
128     prelocal
255     local
254     main
253     default
0       unspec
#
# local
#
#1      inr.ruhep
251     ebgp
~~~


Triem els paquets, l'arquitectura i compilem la imatge:

~~~ {.bash}
make menuconfig
make
~~~

En el cas d'Alix 2D2/2D3 obtindrem la imatge *bin/targets/x86/geode/lede-x86-geode-combined-ext4.img.gz*, la descomprimim i la gravem a una targeta CF:

~~~ {.bash}
gunzip lede-x86-geode-combined-ext4.img.gz
sudo dd if=lede-x86-geode-combined-ext4.img of=/dev/sdX
~~~

amb *gparded* o una eina similar, ampliem la partició fins a ocupar tota l'espai lliure de la CF


## Diagrama funcional dels daemons de routing Bird i BMX6

Per configurar correctament els daemons de routing cal entendre els blocs funcionals de cada programa. Bird defineix de manera genèrica un conjunt de *protocols* representats en el diagrama per blocs. Cada protocol sincronitza els anuncis que rep i els envia a una taula de routing pròpia. Cada taula de Bird està vinculada a una taula de kernel real a través de protocols tipus *kernel*. Cada protocol pot acceptar filtres sobre els prefixes de rutes que intercanvia de manera que pot controlar els prefixos anunciats i acceptats. La sincronització entre taules diferents de Bird es fa amb el protocol *Pipe*.
A la següent figura també es pot apreciar el nom del filtre aplicat en cada vincle funcional.

~~~ {}
        BMX6        |     LINUX KERNEL   |         BIRD
                    |                    |               (export ISNn)  (import ISNn)        
                    |                    |                            ^|
                    |                    |                            |~ (ebgp_in/out)
                    |                    |                        +---------+
                    |                    |                        |   BGP   |
                    |                    |                        |Peer ISNn|
                    |                    |                        +---------+
                    |                    |                            ^|
                    |                    |                            ||
                    |                    |               (import)     |~
     +--------+     |       +-----+      |     +-------+ (all)     +-----+        +---------+
     | Table  |     |       |Table|------+---->|kernel2|---------->|Table|------->|  BGP    |------>(export MXNn)(ibgp_out)
<----| plugin |<----+-------|251  |<-----+-----|       |<----+-----|251  |<-------|Peer MIXn|<------(import MXNn)(ibgp_in)
     +--------+     |       +-----+      |     +-------+     |     +-----+        +---------+
                    |                    |                   |        ^|
                    |                    |                   |        || (import accept_from_peer_ISNn)
                    |                    |        (export)   |        |~ (export reject_no_zone2_prefix)
                    |                    |(reject_from_peer_MXNn)  +-----+
                    |                    |                         |pipe1|
                    |                    |                         +-----+
                    |                    |                            ^|
                    |                    |                            ||
                    |                    |                (import)    |~
     +------+       |       +-----+      |     +-------+   (all)   +------+       +-------+
---->| core |-------+------>|Table|------+---->|kernel1|---------->|Table |       |direct1|
<----|      |<---+  |       |main |<-----+-----|       |<----------|master|<------|       |<------(local ifaces)
     +------+    |  |       +-----+      |     +-------+  (export) +------+       +-------+
                 |                                          (all)
        (local networks)
~~~

BMX6 per la seva banda anuncia els prefixes que té pre-configurats, normalment els corresponents a les interfícies de xarxa *br-lan*. D'una altra banda, importa a la taula *main* els prefixes de la resta d'anuncis del domini BMX6. Els anuncis dels prefixes arribats de Bird, es fa a través del plugin Table referit a la taula d'intercanvi 251.


### Detall de les configuracions finals

Ha calgut crear un conjunt de filtres a Bird per tal d'implementar les següents polítiques destinades a assolir tots els objectius. Hem ubicat l'arxiu de filtres a */etc/bird4/filters/bgp*. Aquest és l'arxiu corresponent a un dels nodes MXN. L'altre és bàsicament el mateix però canviant la variable *krt_prefsrc* per tal de definir l'atribut d'adreça preferent d'origen amb una IP d'una de les interfícies de xarxa. Això permet que els paquets generats pel propi router tingui aquesta IP com origen. Una altre part que depèn del node és la inclusió del filter *reject_from_peer_X*, on *X* és el nom del protocol de BGP intern.

~~~ {}
function match_zone1_prefix() {

        return net ~ [
#                10.1.0.0/21{24,28},
#                10.1.192.0/21{24,28},
#                10.1.72.0/21{24,28},
#                10.1.8.0/21{24,28},
                 10.1.24.0/21{24,28},
                10.139.6.0/23{24,28},
#               10.138.27.0/24{24,28},
                10.139.16.0/20{24,28},
                10.139.36.0/22{24,28},
#               10.139.88.0/21{24,28},
                10.90.224.0/20{24,28},
                10.228.192.0/20{24,28},
                10.38.140.0/22{24,28},
#               10.35.124.0/22{24,28}
        ];

}

function match_zone2_prefix() {

        return net ~ [
                10.1.56.0/21{24,28},
                10.1.192.0/21{24,28}
        ];
}

function match_guifi_prefix() {

        return net ~ [
                10.0.0.0/8{9,28}
        ];
}

filter ebgp_in {

        krt_prefsrc = 10.1.56.193;

        if match_zone1_prefix() then accept;
        else reject;
}

filter ebgp_out {

        if match_guifi_prefix() then accept;
        else reject;

}

filter ibgp_out {

        if match_guifi_prefix() then accept;
        else reject;

}

filter ibgp_in {

        if match_guifi_prefix() then accept;
        else reject;

}

filter reject_no_zone2_prefix {

        if match_zone2_prefix() then accept;
        else reject;

}

filter accept_from_peer_BCNRembrandt {

        if proto="BCNRembrandt" then accept;
        else reject;
}

filter reject_from_peer_BCNLaFabra {

        if proto="BCNLaFabra" then reject;
        else accept;

~~~

Les tres primeres funcions comproven que un determinat prefix pertany o no a una de les tres zones:

- Zona 1: corresponent a prefixes de xarxa situats en lloc geogràficament propers
- Zona 2: corresponent a prefixes continguts dins el domini BMX6 local
- Guifi: corresponent a tot Guifi.net

Si un prefix encaixa en aquestes condicions, la funció retorna un *TRUE*, si no, un *FALSE*. El filtre *ebgp_in* rebutja tots aquells prefixes que no pertanyin a la zona 1. El filtre *ebgp_out* els exporta tots sempre que pertanyin a Guifi.net. Els filtres *ibgp_in/out* permeten incloure a la taula de Bird *ebgp* tots els prefixes provinents del peer BGP intern. Per tant, la taula de Bird *ebgp* (251) contindrà tots els prefixos rebuts des de peers externs dins la zona 1 i els del peer intern, siguin quins siguin, de Guifi.net. El filtre *reject_no_zone2_prefix* s'aplica a la exportació del protocol *pipe1*. És a dir, que la taula *ebgp* no rebrà de la taula Bird *master* cap prefixe que no sigui del domini BMX6 intern. Finalment el filtre *reject_from_peer_BCNLaFabra* evitarà que la taula del kernel *ebgp* (251) contingui rutes que no hagin estat anunciades pel peer extern.

La configuració de Bird d'un node MXN és:

~~~{}
config bird 'bird'
        option use_UCI_config '1'
        option UCI_config_file '/tmp/bird4.conf'

config global 'global'
        option log_file '/tmp/bird4.log'
        option log 'all'
        option router_id '10.1.56.193'
        option debug 'off'

config table
        option name 'ebgp'

config kernel 'kernel2'
        option scan_time '10'
        option learn '1'
        option disabled '0'
        option table 'ebgp'
        option kernel_table '251'
        option import 'all'
        option export 'filter reject_from_peer_BCNLaFabra'

config bgp_template 'bgp_common'
        option import_limit_action 'warn'
        option export_limit_action 'warn'
        option export_limit '3000'
        option receive_limit '3000'
        option import_limit '3000'
        option receive_limit_action 'warn'
        option local_as '49174'
        option import 'all'
        option export 'all'
        option next_hop_self '0'

config bgp 'BCNRembrandt'
        option import_limit_action 'warn'
        option export_limit_action 'warn'
        option receive_limit_action 'warn'
        option template 'bgp_common'
        option import_limit '3000'
        option export_limit '3000'
        option receive_limit '3000'
        option import 'filter ebgp_in'
        option export 'filter ebgp_out'
        option table 'ebgp'
        option neighbor_address '172.25.63.202'
        option neighbor_as '57824'

config filter 'ebgp_default'
        option type 'bgp'
        option file_path '/etc/bird4/filters/bgp'
        option instance 'BCNRembrandt'

config device 'device1'
        option disabled '0'
        option scan_time '10'

config direct 'direct1'
        option disabled '0'
        option interface '"br-lan"'

config bgp 'BCNLaFabra'
        option import_limit_action 'warn'
        option export_limit_action 'warn'
        option receive_limit_action 'warn'
        option template 'bgp_common'
        option import_limit '3000'
        option export_limit '3000'
        option receive_limit '3000'
        option neighbor_as '49174'
        option import 'filter ibgp_in'
        option export 'filter ibgp_out'
        option table 'ebgp'
        option neighbor_address '10.228.204.129'
        option igp_table 'master'
        option next_hop_self '1'

config kernel 'kernel1'
        option disabled '0'
        option learn '1'
        option scan_time '10'
        option import 'all'
        option export 'all'

config pipe 'pipe1'
        option disabled '0'
        option peer_table 'ebgp'
        option export 'filter reject_no_zone2_prefix'
        option import 'filter accept_from_peer_BCNRembrandt'

config table
        option name 'master'

~~~

i per BMX6:

~~~{}
config bmx6 'general'
        option tun4Address '10.1.56.193/27'
        option tun6Address '2012:0:0:a7f9:0:0:0:1/64'

config plugin 'bmx6_config_plugin'
        option plugin 'bmx6_config.so'

config plugin 'bmx6_json_plugin'
        option plugin 'bmx6_json.so'

config plugin 'bmx6_sms_plugin'
        option plugin 'bmx6_sms.so'

config plugin 'bmx6_table_plugin'
        option plugin 'bmx6_table.so'

config syncSms
        option syncSms 'chat'

config ipVersion 'ipVersion'
        option ipVersion '6'

config dev 'mesh'
        option dev 'mesh_12'
        option linklayer '1'

config tunDev 'tmain'
        option tunDev 'tmain'
        option tun6Address '2012:0:0:a7f9:0:0:0:1/64'
        option tun4Address '10.1.56.193/27'

config tunOut 'qmp_cloud'
        option tunOut 'cloud'
        option network '10.0.0.0/8'
        option minPrefixLen '24'

config tunOut 'qmp_cloud6'
        option tunOut 'cloud6'
        option network '::/0'
        option minPrefixLen '48'

config tunOut 'qmp_community6'
        option tunOut 'community6'
        option network '::/0'
        option minPrefixLen '32'
        option maxPrefixLen '48'

config tunIn 'qmp_inet4_offer'
        option tunIn 'inet4_offer'
        option network '0.0.0.0/0'

config tunIn 'qmp_community_offer'
        option tunIn 'community_offer'
        option network '10.0.0.0/8'

config redistTable 'bgp'
        option redistTable 'bgp'
        option table '251'
        option network '10.0.0.0/8'
        option aggregatePrefixLen '24'
        option minPrefixLen '8'
        option maxPrefixLen '28'
        option all '1'
~~~

## Proves i conclusions

En el nostre banc de proves, hem mirat de simular una xarxa com la descrita. En un entorn de producció els encaminadors ISN poden arribar a exportar de l'ordre de 2500 prefixes. Per provar la viabilitat de la plataforma per nodes MXN, hem fet les següents proves:


### Prova amb llista completa de prefixos

Desactivació dels filtres de rebuig de prefixes zonals, és a dir, la taula *ebgp* contenia tots el prefixos possibles, uns 2500. BMX6 en conseqüència examina la taula 251, mira d'agregar prefixes i els anuncia dins del domini intern. El resultat  ha estat l'aturada eventual del daemon BMX6 i l'aparició d'errors del tipus:

~~~ {.syslog}
Fri Jul  1 15:38:57 2016 daemon.err bmx6[928]: INFO  redist_table_routes():  CHANGED out.items=1345 in.items=2111 opt.items=1 net_advs=1345
Fri Jul  1 15:38:57 2016 daemon.err bmx6[928]: WARN  critical system time drift detected: ++ca 11 s, 553578 us! Correcting reference!
Fri Jul  1 15:38:57 2016 daemon.err bmx6[928]: ERROR create_description_tlv_tunXin6_net_adv_msg(): NO description space left for src=fd66:66:66:ff00:20d:b9ff:fe2e:a7f8 dst=::a8a:6200
Fri Jul  1 15:38:57 2016 daemon.err bmx6[928]: ERROR create_description_tlv_tunXin6_net_adv_msg(): NO description space left for src=fd66:66:66:ff00:20d:b9ff:fe2e:a7f8 dst=::a8a:8d00
Fri Jul  1 15:38:57 2016 daemon.err bmx6[928]: WARN  muting further messages (with equal first 30 bytes) for at most 100 seconds
Fri Jul  1 15:38:57 2016 daemon.err bmx6[928]: WARN  create_description_tlv_tunXin6_net_adv(): created 153 of 1348 v4 advs due to lack of description space!!
Fri Jul  1 15:39:21 2016 daemon.err bmx6[928]: INFO  redist_table_routes():  CHANGED out.items=1344 in.items=2110 opt.items=1 net_advs=1344
Fri Jul  1 15:39:21 2016 daemon.err bmx6[928]: WARN  critical system time drift detected: ++ca 20 s, 534118 us! Correcting reference!
Fri Jul  1 15:39:21 2016 daemon.err bmx6[928]: WARN  create_description_tlv_tunXin6_net_adv(): created 153 of 1347 v4 advs due to lack of description space!!
Fri Jul  1 15:39:45 2016 daemon.err bmx6[928]: INFO  redist_table_routes():  CHANGED out.items=1343 in.items=2109 opt.items=1 net_advs=1343
Fri Jul  1 15:39:45 2016 daemon.err bmx6[928]: WARN  critical system time drift detected: ++ca 20 s, 332879 us! Correcting reference!
Fri Jul  1 15:39:45 2016 daemon.err bmx6[928]: WARN  create_description_tlv_tunXin6_net_adv(): created 153 of 1346 v4 advs due to lack of description space!!
Fri Jul  1 15:40:08 2016 daemon.err bmx6[928]: INFO  redist_table_routes():  CHANGED out.items=1343 in.items=2109 opt.items=1 net_advs=1343
Fri Jul  1 15:40:08 2016 daemon.err bmx6[928]: WARN  critical system time drift detected: ++ca 19 s, 870972 us! Correcting reference!
Fri Jul  1 15:40:08 2016 daemon.err bmx6[928]: WARN  create_description_tlv_tunXin6_net_adv(): created 153 of 1346 v4 advs due to lack of description space!!
~~~

i un consum de CPU molt alt:

~~~{}
Mem: 20848K used, 233720K free, 700K shrd, 712K buff, 8452K cached
CPU: 100% usr   0% sys   0% nic   0% idle   0% io   0% irq   0% sirq
Load average: 0.54 0.30 0.14 2/47 18928
  PID  PPID USER     STAT   VSZ %VSZ %CPU COMMAND
  928     1 root     R     1936   1% 100% /usr/sbin/bmx6 -f /etc/config/bmx6 -d
~~~

**Conclusió** La versió de BMX6 provada no és capaç d'anunciar de l'ordre de 2500 prefixos. Les possibles raons serien que s'assoleix la mida màxima del descriptor i que el procés d'agregació automàtic consumeix una quantitat enorme de recursos. Del missatge d'error

~~~{}
Fri Jul  1 15:39:45 2016 daemon.err bmx6[928]: WARN  create_description_tlv_tunXin6_net_adv(): created 153 of 1346 v4 advs due to lack of description space!!
~~~

es dedueix que la versió provada de BMX6 no admet més de 153 anuncis de prefixes en un sol descriptor.

### Prova amb llista parcial de prefixos

Enlloc d'anunciar tots el 2500 prefixos de xarxa, només anunciem per iBGP i dins el domini BMX6 una part. En concret els prefixes que es trobem més propers geogràficament. A l'anterior arxiu de filtres, a la funció *match_zone1_prefix* només permet la importació de prefixos de l'àrea del Barcelonés i les seves zones mesh. En conseqüència l'anunci iBGP i BMX6 només transfereixen els prefixos que encaixen. En el nostre cas obtenim un total de 197 prefixos anunciats per iBGP i 142 (amb agregació de rutes) per BMX6.

~~~{}
Mem: 16272K used, 238296K free, 152K shrd, 572K buff, 6320K cached
CPU:   0% usr   0% sys   0% nic  99% idle   0% io   0% irq   0% sirq
Load average: 0.01 0.01 0.00 1/42 2084
  PID  PPID USER     STAT   VSZ %VSZ %CPU COMMAND
 1721     1 root     S     1400   1%   0% /usr/sbin/bmx6 -f /etc/config/bmx6 -d
~~~

Un problema indirecte conseqüència de l'increment del número de prefixes anunciats, és que el firmware QMP, té problemes per per mostrar la llista completa dels túnels BMX6 per la interfície web de gestió. Això, passa en els nodes de tipus Nanostation M5.

**Conclusió:** Amb 197 rutes a la taula de intercanvi i 142 anuncis agregats, el BMX6 no presenta cap problema de bloqueig i consum de recursos, tal com s'esperava en no superar els 153 anuncis.

## 001-filters_fix_new_protocols.patch

```diff
--- a/src/config/bird4
+++ b/src/config/bird4
@@ -41,7 +41,7 @@ config bgp bgp1
     option source_address '172.16.1.6'
     option next_hop_self '0'
     option next_hop_keep '0'
-    option rr_client '1'
+    option rr_client '0'
     option rr_cluster_id '172.16.1.6'

 config bgp_template bgp_common
--- a/src/init.d/bird4
+++ b/src/init.d/bird4
@@ -1,6 +1,6 @@
 #!/bin/sh /etc/rc.common

-# Copyright (C) 2014 - Eloi Carbó Solé (GSoC2014)
+# Copyright (C) 2014 - Eloi Carbó Solé (GSoC2014)
 # BGP/Bird integration with OpenWRT and QMP
 #
 # This program is free software: you can redistribute it and/or modify
@@ -42,7 +42,7 @@ writeToConfig() {
 # $1 string. $2 string.
 # This function checks if $2 is empty. If not, it writes the string $1 in the $BIRD_CONFIG file.
 # Use write function to check if $1, value found inside $2, is not empty and can be written in the configuration file.
-# Example: N=""; write "value: $N" $N;
+# Example: N=""; write "value: $N" $N;
 write() {
     [ -n "$2" ] && writeToConfig "$1"
 }
@@ -101,13 +101,13 @@ prepare_global () {

     # Remove old configuration file
     rm -f "$BIRD_CONFIG"
-
+
     get log_file $section
     get log $section
     get debug $section
     get router_id $section
     get table $section
-
+
     # First line of the NEW configuration file
     echo "#Bird4 configuration using UCI:" > $BIRD_CONFIG
     writeToConfig " "
@@ -176,7 +176,7 @@ prepare_kernel() {
     get kernel_table $section
     get learn $section
     get persist $section
-    writeToConfig "protocol kernel {"
+    writeToConfig "protocol kernel $section {" $section
     write_bool disabled $disabled
     write "    table $table;" $table
     write "    kernel table $kernel_table;" $kernel_table
@@ -214,7 +214,7 @@ prepare_static() {
 # This function gets each "device" protocol section in the UCI configuration and sets each option in the bird4.conf file.
 # $1 is set as the ID of the current UCI device section.
 prepare_device() {
-    local section="$1"
+    local section="$1"
     local disabled; local scan_time
     get disabled $section
     get scan_time $section
@@ -226,6 +226,50 @@ prepare_device() {
     writeToConfig " "
 }

+
+# Function: prepare_direct $1
+# $1 string
+# This function gets each "direct" protocol section in the UCI configuration and sets each option in the bird4.conf file.
+# $1 is set as the ID of the current UCI direct section.
+prepare_direct() {
+    local section="$1"
+    local disabled; local interface
+    get disabled $section
+    get interface $section
+    write "#$section configuration:" $section
+    writeToConfig "protocol direct {"
+    write_bool disabled $disabled
+    write "    interface $interface;" $interface
+    writeToConfig "}"
+    writeToConfig " "
+}
+
+# Function: prepare_pipe $1
+# $1 string
+# This function gets each "pipe" protocol section in the UCI configuration and sets each option in the bird4.conf file.
+# $1 is set as the ID of the current UCI direct section.
+prepare_pipe() {
+    local section="$1"
+    local disabled; local table; local peer_table; local mode; local import; local export
+    get disabled $section
+    get peer_table $section
+    get mode $section
+    get table $section
+    get import $section
+    get export $section
+    write "#$section configuration:" $section
+    writeToConfig "protocol pipe $section {" $section
+    write_bool disabled $disabled
+    write "    table $table;" $table
+    write "    peer table $peer_table;" $peer_table
+    write "    mode $mode;" $mode
+    write "    import $import;" $import
+    write "    export $export;" $export
+    writeToConfig "}"
+    writeToConfig " "
+}
+
+
 # Function: prepare_bgp_template $1
 # $1 string
 # This function gets each "bgp_template" protocol section in the UCI configuration and sets each option in the bird4.conf file.
@@ -252,7 +296,7 @@ prepare_bgp_template() {
     get receive_limit_action $section
     get neighbor_address $section
     get neighbor_as $section
-
+
     writeToConfig "#$section template:"
     writeToConfig "template bgp $section {"
     [ -n "$disabled" ] && write_bool disabled $disabled
@@ -312,7 +356,7 @@ prepare_bgp() {
     get receive_limit_action $section
     get neighbor_address $section
     get neighbor_as $section
-
+
     writeToConfig "#$section configuration:"
     [ -n "$template" ] && writeToConfig "protocol bgp $section from $template {" || writeToConfig "protocol bgp $section {"
     [ -n "$disabled" ] && write_bool disabled $disabled
@@ -347,15 +391,15 @@ prepare_bgp() {
     writeToConfig " "
 }

-# Function: prepare_bgp_filters $1
+# Function: prepare_filters $1
 # $1 string
 # This function gets each "bgp_filter" protocol section in the UCI configuration and sets each option in the bird4.conf file.
 # $1 is set as the ID of the current UCI bgp_filter section.
 # This function checks if the filter file exists and, in that case, it writes its content to the configuration file.
-prepare_bgp_filters() {
+prepare_filters() {
     local section="$1"
     local type
-    local file_path
+    local file_path
     get type $section
     get file_path $section
     if [ -e "$file_path" ]; then
@@ -372,25 +416,27 @@ start() {
     config_load bird4
     local use_UCI_config
     get use_UCI_config 'bird'
-
+
     if [ -z "$use_UCI_config" -o "$use_UCI_config" = "0" ]; then
         service_start $BIRD_BIN -d -c $BIRD_CONFIG -P $SERVICE_PID_FILE
     else
         #Set Bird4 configuration location:
         local UCI_config_File
         get UCI_config_File 'bird'
-        BIRD_CONFIG=${UCI_config_File:-/tmp/bird4.conf}
+        BIRD_CONFIG=${UCI_config_file:-/tmp/bird4.conf}
         #Setup the basic configuration
         prepare_global 'global'
+	config_foreach prepare_filters 'filter'
         config_foreach prepare_kernel 'kernel'
         config_foreach prepare_static 'static'
         config_foreach prepare_device 'device'
-        #config_foreach prepare_direct 'direct'
-
+        config_foreach prepare_direct 'direct'
+	config_foreach prepare_pipe 'pipe'
+
         #Setup the protocols configuration (currently BGP only)
         config_foreach prepare_bgp_template 'bgp_template'
         config_foreach prepare_bgp 'bgp'
-        config_foreach prepare_bgp_filters 'filter'
+
         #Start the service
         service_start $BIRD_BIN -d -c $BIRD_CONFIG -P $SERVICE_PID_FILE
     fi
--- a/src/model/overview.lua
+++ b/src/model/overview.lua
@@ -30,7 +30,7 @@ s_bird_uci.addremove = False

 uuc = s_bird_uci:option(Flag, "use_UCI_config", "Use UCI configuration", "Use UCI configuration instead of the /etc/bird4.conf file")

-ucf = s_bird_uci:option(Value, "UCI_config_File", "UCI File", "Specify the file to place the UCI-translated configuration")
+ucf = s_bird_uci:option(Value, "UCI_config_file", "UCI File", "Specify the file to place the UCI-translated configuration")
 ucf.default = "/tmp/bird4.conf"

 -- Named Section: "table"
@@ -50,25 +50,27 @@ id = s_bird_global:option(Value, "router

 lf = s_bird_global:option(Value, "log_file", "Log File", "File used to store log related data.")

-l = s_bird_global:option(MultiValue, "log", "Log", "Set which elements do you want to log.")
+l = s_bird_global:option(ListValue, "log", "Log", "Set which elements do you want to log.")
+l:value("off", "Off")
 l:value("all", "All")
-l:value("info", "Info")
-l:value("warning","Warning")
-l:value("error","Error")
-l:value("fatal","Fatal")
-l:value("debug","Debug")
-l:value("trace","Trace")
-l:value("remote","Remote")
-l:value("auth","Auth")
+l:value("{ info }", "Info")
+l:value("{ warning }","Warning")
+l:value("{ error }","Error")
+l:value("{ fatal }","Fatal")
+l:value("{ debug }","Debug")
+l:value("{ trace }","Trace")
+l:value("{ remote }","Remote")
+l:value("{ auth }","Auth")

-d = s_bird_global:option(MultiValue, "debug", "Debug", "Set which elements do you want to debug.")
+d = s_bird_global:option(ListValue, "debug", "Debug", "Set which elements do you want to debug.")
+d:value("off", "Off")
 d:value("all", "All")
-d:value("states","States")
-d:value("routes","Routes")
-d:value("filters","Filters")
-d:value("interfaces","Interfaces")
-d:value("events","Events")
-d:value("packets","Packets")
+d:value("{ states }","States")
+d:value("{ routes }","Routes")
+d:value("{ filters }","Filters")
+d:value("{ interfaces }","Interfaces")
+d:value("{ events }","Events")
+d:value("{ packets }","Packets")

 function m.on_commit(self,map)
         luci.sys.call('/etc/init.d/bird4 stop; /etc/init.d/bird4 start')
--- a/Makefile
+++ b/Makefile
@@ -58,7 +58,7 @@ endef

 define Package/$(uci)/postinst
 #!/bin/sh
-if [ -z $${IPKG_INSTROOT} ]; then
+if [ -z "$${IPKG_INSTROOT}" ]; then
     ( . /etc/bird4/init.d/bird4-uci-install-init.d ) && rm -f /etc/bird4/init.d/bird4-uci-install-init.d
 fi
 endef
--- a/src/controller/bird4.lua
+++ b/src/controller/bird4.lua
@@ -21,7 +21,7 @@ module("luci.controller.bird4", package.
 function index()
         entry({"admin","network","bird4"}, cbi("bird4/overview"), "Bird4", 0).dependent=false
         entry({"admin","network","bird4","overview"}, cbi("bird4/overview"), "Overview", 1).dependent=false
-        entry({"admin","network","bird4","proto_general"}, cbi("bird4/gen_proto"), "General protocols", 3).dependent=false
+        entry({"admin","network","bird4","proto_general"}, cbi("bird4/gen_proto"), "General Protocols", 3).dependent=false
         entry({"admin","network","bird4","proto_bgp"}, cbi("bird4/bgp_proto"), "BGP Protocol", 4).dependent=false
 end

--- a/src/model/gen_proto.lua
+++ b/src/model/gen_proto.lua
@@ -1,5 +1,5 @@
---[[
-Copyright (C) 2014 - Eloi Carbó Solé (GSoC2014)
+--[[
+Copyright (C) 2014 - Eloi Carbó Solé (GSoC2014)
 BGP/Bird integration with OpenWRT and QMP

 This program is free software: you can redistribute it and/or modify
@@ -25,13 +25,17 @@ m=Map("bird4", "Bird4 general protocol's

 -- Optional parameters lists
 local protoptions = {
-	{["name"]="table", ["help"]="Auxiliar table for routing", ["depends"]={"static","kernel"}},
-	{["name"]="import", ["help"]="Set if the protocol must import routes", ["depends"]={"kernel"}},
-	{["name"]="export", ["help"]="Set if the protocol must export routes", ["depends"]={"kernel"}},
+	{["name"]="table", ["help"]="Auxiliar table for routing", ["depends"]={"static","kernel","pipe"}},
+	{["name"]="import", ["help"]="Set if the protocol must import routes", ["depends"]={"kernel","pipe"}},
+	{["name"]="export", ["help"]="Set if the protocol must export routes", ["depends"]={"kernel","pipe"}},
 	{["name"]="scan_time", ["help"]="Time between scans", ["depends"]={"kernel","device"}},
 	{["name"]="kernel_table", ["help"]="Set which table must be used as auxiliar kernel table", ["depends"]={"kernel"}},
 	{["name"]="learn", ["help"]="Learn routes", ["depends"]={"kernel"}},
-	{["name"]="persist", ["help"]="Store routes. After a restart, routes will be still configured", ["depends"]={"kernel"}}
+	{["name"]="persist", ["help"]="Store routes. After a restart, routes will be still configured", ["depends"]={"kernel"}},
+	{["name"]="primary", ["help"]="Allows to specify which network address should be chosen as a primary one", ["depends"]={"device"}},
+	{["name"]="interface", ["help"]="Restrict generated routes to some subset of interfaces or addresses", ["depends"]={"direct"}},
+	{["name"]="peer_table", ["help"]="Defines secondary routing table to connect to", ["depends"]={"pipe"}},
+	{["name"]="mode", ["help"]="Specifies the mode for the pipe to work in", ["depends"]={"pipe"}}
 }

 local routeroptions = {
@@ -62,7 +66,7 @@ for _,o in ipairs(protoptions) do
 			if d == "kernel" then
 				if o.name == "learn" or o.name == "persist" then
 					value = sect_kernel_protos:option(Flag, o.name, translate(o.name), translate(o.help))
-				elseif o.name == "table" then
+				elseif o.name == "table" then
 					value = sect_kernel_protos:option(ListValue, o.name, translate(o.name), translate(o.help))
 					uciout:foreach("bird4", "table",
 						function (s)
@@ -105,7 +109,80 @@ for _,o in ipairs(protoptions) do
 		end
 	end
 end
-																												
+
+--
+-- DIRECT PROTOCOL
+--
+
+sect_direct_protos = m:section(TypedSection, "direct", "Direct options", "Configuration of the direct protocols.")
+sect_direct_protos.addremove = true
+sect_direct_protos.anonymous = false
+
+-- Default kernel parameters
+
+disabled = sect_direct_protos:option(Flag, "disabled", "Disabled", "If this option is true, the protocol will not be configured.")
+disabled.default=0
+
+-- Optional parameters
+for _,o in ipairs(protoptions) do
+	if o.name ~= nil then
+		for _, d in ipairs(o.depends) do
+			if d == "direct" then
+				value = sect_direct_protos:option(Value, o.name, translate(o.name), translate(o.help))
+				value.optional = true
+				value.rmempty = true
+			end
+		end
+	end
+end
+
+
+--
+-- PIPE PROTOCOL
+--
+
+sect_pipe_protos = m:section(TypedSection, "pipe", "Pipe options", "Configuration of the pipe protocols.")
+sect_pipe_protos.addremove = true
+sect_pipe_protos.anonymous = false
+
+-- Default pipe parameters
+disabled = sect_pipe_protos:option(Flag, "disabled", "Disabled", "If this option is true, the protocol will not be configured.")
+disabled.default=0
+
+-- Optional parameters
+
+for _,o in ipairs(protoptions) do
+        if o.name ~= nil then
+                for _, d in ipairs(o.depends) do
+                        if d == "pipe" then
+				if o.name == "table" then
+     					value = sect_pipe_protos:option(ListValue, o.name, translate(o.name), translate(o.help))
+                                        uciout:foreach("bird4", "table",
+                                                function (s)
+                                                        value:value(s.name)
+                                                end)
+                                        value:value("")
+                                elseif o.name == "peer_table" then
+					value = sect_pipe_protos:option(ListValue, o.name, translate(o.name), translate(o.help))
+                                        uciout:foreach("bird4", "table",
+                                                function (s)
+                                                        value:value(s.name)
+					end)
+                                        value:value("")
+				elseif o.name == "mode" then
+					value = sect_pipe_protos:option(ListValue, o.name, translate(o.name), translate(o.help))
+					value:value("opaque", "Opaque")
+					value:value("transparent", "Transparent")
+                                else
+                                        value = sect_pipe_protos:option(Value, o.name, translate(o.name), translate(o.help))
+                                end
+                                value.optional = true
+                                value.rmempty = true
+			end
+         	end
+        end
+end
+
 --
 -- STATIC PROTOCOL
 --
```
