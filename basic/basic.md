# Què és guifi?

Actualment és un arbre de 5 branques:

- La branca social. Una comunitat rica, diversa, heterogènia, complexa. Un conjunt d'individus i organitzacions amb interessos comuns: la xarxa. Els actors o grups més representatius són els usuaris (utilitzen la xarxa), els voluntaris (contribueixen sense garanties) i els professionals (contribueixen amb garanties).

- La branca tecnològica. Una xarxa de telecomunicacions. Una xarxa física d'ubicacions amb antenes, cables, racks, servidors, switchos, routers (encaminadors), i altres equips de telecomunicacions que estableixen enllaços amb wifi i fibra òptica per tal de generar una xarxa lògica: un mapa de rutes per arribar a tots els indrets que formen part de guifi a través dels mateixos protocols que governen Internet. Tot plegat genera moltíssimes possibilitats i flexibilitat al voltant de la gran pregunta: A qui comprar o amb qui compartir Internet?. La opció més autònoma és la de la Fundació Guifi, operador majorista, que compra l'interconnexió de guifi a Internet i comparteix els costos amb diferents organitzacions (associacions, operadors, etc.) que formen part de guifi per a que distribueixin Internet als usuaris de guifi.

- La branca econòmica. Una infraestructura de comuns, un [Common Pool Resource (CPR)](https://en.wikipedia.org/wiki/Common-pool_resource). La comunitat té com a mecanisme la [llicència de Comuns](https://guifi.net/ComunsXOLN) i l'aplicació web de guifi.net per tal de regular i gestionar la xarxa. La Fundació Guifi dóna les garanties legals.

- La branca internacional. Un model de referència, bones pràctiques, experiències, guifi com a cas d'èxit. Relació de guifi amb la [resta de comunitats en xarxa arreu del món](https://en.wikipedia.org/wiki/List_of_wireless_community_networks_by_region).

- La branca experimental. Un laboratori d'experimentació. Guifi dona flexibilitat, i això l'ha fet escenari de diferents projectes de recerca europeus, universitaris, etc.

# Por qué guifi está tan extendido en los pueblos?

Porque los operadores de telecomunicacions son esencialmente grandes multinacionales y no invierten en zonas rurales

artículos que reflejan la situación:

- [Cero G, el mapa de la España sin wifi](http://www.elmundo.es/sociedad/2017/04/24/58fa3de946163f36758b4639.html)

# De què depén que em pugui connectar a guifi?

## Ubicació i cobertura

Si t'has registrat a la pàgina de guifi.net, en la pestanya distàncies podràs veure a quina distància tens el node més proper. Necessites que aquest node al que vols connectar-te sigui supernode (amb una estrella verda al mapa) o node mesh (punt vermell al mapa).

Si des de la ubicació actual fins a tu hi ha menys de 200 metres probablement et podràs connectar satisfactòriament de qualsevol manera.

La visió directa i les [zones de fresnel](https://en.wikipedia.org/wiki/Fresnel_zone) importaran progressivament amb l'increment de la distància.

Si tens dubtes, fes fotos (idealment panoràmica) de la ubicació on vols posar el node i consulta-ho amb la comunitat: llistes de correu, trobades presencials (guifilabs) o el xat.

## Pressupost

El cost d'un node de guifi no és car, però tampoc és tant barat per assumir-lo de cop. Es necessita com a mínim una partida de 150 € per poder cobrir els costos més essencials, i més si la nostra instal·lació es especial o si volem que la faci un professional (pagar la mà d'obra).

## Relacions socials

Una bona relació amb els veïns i amb els que connectarem serà molt positiva. Per exemple: ens poden ajudar a compartir els gastos que el node suposa, ens poden donar suport en el cas de demanar permís per posar el node en una comunitat de veïns conflictiva, ens poden autoritzar posar un altre node de guifi a casa seva per a que així ens arribi la cobertura.

Nota: Hi ha una regla a guifi que és que l'últim que es connecta paga lo que faci falta, en el sentit que si s'ha de fer una millora per a que et puguis connectar, la paga el que acaba d'arribar. Hi ha una excepció que seria quan algú en concret té grans interessos en que es faci la instal·lació de guifi a casa teva.

# Internet des de guifi

Internet és una xarxa de xarxes on Guifi forma part a través de la [Fundació Guifi](https://stat.ripe.net/AS49835#tabId=at-a-glance). Guifi alhora és una xarxa de xarxes. Per arribar a altres indrets de Guifi tan sols has d'estar connectat, però per arribar a altres indrets d'Internet o has de pagar-ho o algú ho ha de pagar. Guifi et dona moltíssima flexibilitat per a que decideixis a qui pagar, si te'l paguen, o amb qui comparteixes el cost d'accedir a Internet.

Hi ha dos grans escenaris

- Internet sense garanties (o amb les teves garanties): quan algú te l'està pagant, un grup particular compartiu gastos, o és una solució casolana.
    - Proxy federat: accés a Internet limitat a `http://` i `https://`
    - Sortida directa: a través d'una xarxa mesh, d'un tunel OpenVPN o derivats.

- Internet amb garanties: a través d'un operador de telecomunicacions de guifi. L'operador et determinarà quin tipus de garanties et pot donar per proveïr-te d'Internet i a quin preu.

# Com em connecto al router o l'antenna?

Normalment et connectes de forma automàtica al router (DHCP), i aquest et proveeix de la porta d'enllaç (gateway) per defecte.

Pots accedir a aquesta informació de diferent manera en funció del teu sistema operatiu.

## GNU/Linux

Obre una terminal i pica:

`ip route show`

La sortida té diverses línies, la primera diu una cosa així:

`default via 192.168.1.1 (...)`

En aquest cas, la porta d'enllaç és la `192.168.1.1`. Aquesta ip la utilitzarem per accedir al router des del navegador o `ssh` (terminal remota) i configurar-lo. La ip que ha servit d'exemple és la que acostuma a ser en la majoria de routers domèstics.

## Windows

Inicio, ejecutar, `cmd` i pica:

`ipconfig`

Busca per porta d'enllaç predeterminada o gateway (en funció de l'idioma). Aquesta ip que surt és la que hem d'utilitzar

# Història de guifi

Guifi ve de GUrb wiFI, és la xarxa de telecomunicacions que van començar a desplegar voluntaris al 2004 en Gurb. [En aquest vídeo un dels cofundadors de Guifi explica les motivacions de tot plegat](https://www.youtube.com/watch?v=d_oTloORR30). 2004 és un any on [sorgeixen moltes iniciatives de xarxes comunitàries arreu del món](https://en.wikipedia.org/wiki/List_of_wireless_community_networks_by_region) degut a l'interès creixent per la tecnologia wifi com a nova forma de fer arribar internet a zones amb deficients infraestructures de telecomunicacions. Guifi.net va tenir un tret diferenciador de les altres xarxes comunitàries properes: la seva capacitat tecnològica en forma d'una aplicació web per gestionar la operativa de la xarxa. Va idear el `unsolclic` com una forma d'automatitzar i ajudar en la configuració de l'antena a nous usuaris. Això va provocar que els altres projectes similars utilitzessin també la mateixa web per tal de beneficiar-se. L'any 2007 el projecte guifi.net guanya el premi nacional de telecomunicacions de la Generalitat de Catalunya. Per tal de recollir el premi en metàl·lic cal una organització. Alguns decideixen muntar la Fundació Privada per a la Xarxa Lliure, Oberta i Neutral guifi.net. Aquesta fundació esdevindria poc a poc un operador de telecomunicacions majorista d'Internet i regulador dels diferents actors de la xarxa.

Fets importants:

- 2004 Inici
- 2008 Fundació
- 2012 Primers desplegaments de fibra òptica

## Comunitats en xarxa que es van integrar a guifi

- Badalona Wireless
- Hospitalet Wireless
- Gràcia Sense Fils
- Xarxa Sense Fils Coooperativa (xspcoop)
- Mataró Sense Fils
- RedLibre
