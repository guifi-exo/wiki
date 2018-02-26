# Mapes de les xarxes mesh

- http://dsg.ac.upc.edu/qmpmon/
- http://sants.guifi.net/maps/
- http://libremap.net/

# qMp

## No puc accedir per IPv4 al qMp

Requeriments: accés a l'antena a través de cable (capa dos, link layer). És a dir, tenim un cable al portàtil i a l'altre banda hi ha l'antena o un switch fins l'antena (cap router enmig).

Si cumplim els requeriments podrem fer servir la IPv6 link local per accedir a l'antena i reiniciar-la. Per a tals efectes, hem d'estar connectats a l'antena per IPv6 (el network manager té una opció de link-local only), també va bé un altre intent de connexió habitual IPv4, però es pitjor ja que quan arribi el timeout ens desconnectarà.

```
ping6 ff02::1%eth0
PING ff02::1%wlan0(ff02::1) 56 data bytes
64 bytes from fe80::a8f0:a718:5962:b53: icmp_seq=1 ttl=64 time=0.040 ms
64 bytes from fe80::8fff:d3e:9b72:dcb4: icmp_seq=1 ttl=64 time=2.58 ms (DUP!)
64 bytes from fe80::a8f0:a718:5962:b53: icmp_seq=2 ttl=64 time=0.071 ms
64 bytes from fe80::8fff:d3e:9b72:dcb4: icmp_seq=2 ttl=64 time=2.83 ms (DUP!)
64 bytes from fe80::a8f0:a718:5962:b53: icmp_seq=3 ttl=64 time=0.084 ms
64 bytes from fe80::8fff:d3e:9b72:dcb4: icmp_seq=3 ttl=64 time=2.98 ms (DUP!)
```

La resposta DUP ens diu que hi ha diversos dispositius que han respost al pong del ping. En aquest cas han sigut 2 (dos IPv6 diferents), i mínim seran 2: nosaltres i l'altre extrem. Agafem la IPv6 del dispositiu que ha fet més latència, vol dir que és l'altre banda.

Llavors ja ens podem connectar a l'antena per ssh:

`ssh root@fe80::8fff:d3e:9b72:dcb4%eth0`

Podem intentar recuperar l'accés de diferents maneres. La més extrema consisteix a borrar el següent fitxer. Això provocarà que l'antena després de reiniciar-se torni als paràmetres per defecte:

`rm /qmp_configured`

reiniciem:

`reboot`

## Analitzar tràfic wireshark de forma còmode

Normalment el procés per capturar tràfic és:

1. Fer ssh a la màquina
2. Capturar amb tcpdump en un fitxer
3. Moure el fitxer a l'ordinador local amb scp

Hi ha però una manera de fer-ho només amb una comanda:

`ssh root@<ip> tcpdump -U -s0 -w - 'not port 22' | wireshark -k -i -`

src http://www.commandlinefu.com/commands/view/4373/analyze-traffic-remotely-over-ssh-w-wireshark

## Obtenció del firmware

per binari o compil·lació

```
The qMp 3.2.1 firmware binaries can be found at http://fw.qmp.cat/Releases/3.2.1. Otherwise, you can compile your own images with your preferred options:

git clone git://qmp.cat/qmpfw.git qmpfw-3.2.1
cd qmpfw-3.2.1
git fetch --tags
git checkout tags/v3.2.1
git checkout -b v3.2.1
QMP_GIT_BRANCH=v3.2.1 make checkout
cd build/qmp && git checkout -b v3.2.1 && cd ../..
make J=n T=target

where n is the number of parallel threads to use in the compilation (1, 2, ..., 8...) and targets is the name of the device target to build the image (list them by issuing the command make list_targets).
```
