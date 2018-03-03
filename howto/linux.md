# openwrt i lede

scan operation

iw dev wlan0 scan

iwinfo wlan0 scan

# Linux i debian

## adreçament estàtic

suposem que tenim el rang de guifi de `10.1.1.0/27` en el nostre node, l'enrutador de guifi té la `10.1.1.1` i el servidor la `10.1.1.2`.

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

suposem que volem que el tràfic que ve de la IP `192.168.98.2` volem que s'enviï per la `192.168.98.1`. I que ho farem a través de la taula1 que la posarem en `252`

Llavors, afegir `taula1 252` a `/etc/iproute2/rt_tables`

en debian, `/etc/network/interfaces` hauria de ser de l'estil (està incomplet):

```
auto eth0 
iface eth0 #?
    # (...)
    up ip route add table taula1 default via 192.168.98.1
    up ip rule add from 192.168.98.2 lookup table taula1
    down ip route del table taula1 default via 192.168.98.1
    down ip rule del from 192.168.98.2 lookup table taula1
```

checkers:

```
# ip route show table taula1
default via 192.168.98.1 dev eth0 
```

ip rule list

ip rule s

### two IPs in different network interfaces of a VM

you want to waste two IPs in the same VM, and make it reachable

quick tips (check src for better info). substitute the values between <>

```
auto ethX
iface ethX inet static
        address <hostip>
        netmask 255.255.255.224
        post-up ip rule add to <hostip> lookup <tablename>
        post-up ip route add default via <gatewayip> dev eth1 table <tablename>
```

```
cat /etc/iproute2/rt_tables
#
# reserved values
#
255 local
254 main
253 default
0   unspec
#
# local
#
#1  inr.ruhep
200 <tablename>
```

reboot

src https://blog.scottlowe.org/2013/05/29/a-quick-introduction-to-linux-policy-routing/

## queries routing

`ip route show table <taula>`

(abreviació: `ip r s t <taula>`


`ip route get <ip>` només consulta la taula main

(abreviació: `ip r g <ip>`
