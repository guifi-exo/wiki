# Linux i debian

## adreçament estàtic

suposem que tenim el rang de guifi de 10.1.1.0/27 en el nostre node, l'enrutador de guifi té la 10.1.1.1 i el servidor la 10.1.1.2

la forma més fàcil d'enrutar el tràfic de guifi cap a guifi és a través d'una ruta estàtica en la interfície a través de l'interfície que està a la xarxa guifi

en debian hauríem de tenir `/etc/network/interfaces` semblant a:

```
auto eth0 
iface eth0 inet static
    address 10.1.1.2
    netmask 255.255.255.240
    gateway 10.1.1.1
    up ip route add 10.0.0.0/8 via 10.1.1.1 dev eth0
    down ip route del 10.0.0.0/8 via 10.1.1.1 dev eth0
```

## policy routing

suposem que volem que el tràfic que ve de la IP 192.168.98.2 volem que s'enviï per la 192.168.98.1. I que ho farem a través de la taula1

afegir la taula1 a les taules de rutes:
echo "taula1 252" >> /etc/iproute2/rt_tables

en debian, `/etc/network/interfaces` hauria de ser de l'estil (està incomplet):

```
auto eth0 
iface eth0 #?
    # (...)
    up ip route add table taula1 default via 192.168.98.1
    up ip rule add from 192.168.98.2 from table taula1
    down ip route del table taula1 default via 192.168.98.1
    down ip rule del from 192.168.98.2 from table taula1
```
