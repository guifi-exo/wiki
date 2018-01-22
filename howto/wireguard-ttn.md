# Generació de firmwares de VPN per TTN-Guifi.net per dispositius LEDE/OpenWRT

Segons la documentació de tunneldigger, cal compilar una imatge de LEDE/OpenWRT per tal d'obtenir el opkg. Recordem els passos bàsics. Clonem el repositori de LEDE:
```
git clone https://git.lede-project.org/source.git lede
```
Això crearà un directori anomenat `lede` on hi tindrem tots els arxius de compilació. Explorem els tags del repositori ja que per defecte el HEAD apunta cap al darrer commit de la versió experimental. Triem la darrera estable:
```
git checkout tags/v17.01.4
```
Tot seguit poden actualitzar i instal·lar els directoris dels paquets dels *feeds*. Triem els paquets .... que considerem oportuns amb *Menuconfig*.
```
./scripts/feeds update -a
./scripts/feeds install -a

make menuconfig
```
Instal·lem els paquets de wireguard i supot luci:
```
root@LEDE:~# opkg install wireguard luci-proto-wireguard luci-app-wireguard
```
La configuració de referència pel *Gateway-keeper* és:
```
config globals 'globals'

config interface 'lan'
        option type 'bridge'
        option proto 'static'
        option netmask '255.255.255.0'
        option ip6assign '60'
        option _orig_ifname 'eth0 wlan0'
        option _orig_bridge 'true'
        option ifname 'eth0'
        option ipaddr '172.16.1.1'

config interface 'wan'
        option ifname 'eth1'
        option _orig_ifname 'eth1'
        option _orig_bridge 'false'
        option proto 'static'
        option ipaddr '10.228.193.115'
        option netmask '255.255.255.224'
        option dns '10.228.203.104'

config interface 'ttn'
        option proto 'wireguard'
        option private_key '6Jm4kaReQsnuyNva4wvg8D3F8V7ZbFvUB5EHpy3h73ax'
        option listen_port '45955'
        option mtu '1396'
        list addresses '172.31.0.3/22'

config wireguard_ttn
        list allowed_ips '0.0.0.0/0'
        option endpoint_host '10.38.140.235'
        option endpoint_port '45955'
        option public_key 'LBW/StqTmQdJLWeWuIUYNkRbSFa3s3RGe7MdeLrV01E='

config route
        option interface 'wan'
        option target '10.0.0.0'
        option netmask '255.0.0.0'
        option gateway '10.228.193.97'
```
Pel que fa al *TTN Broker* tenim:
```
config globals 'globals'

config interface 'lan'
        option type 'bridge'
        option ifname 'eth0'
        option proto 'static'
        option ipaddr '10.38.140.235'
        option netmask '255.255.255.224'
        option ip6assign '60'
        option dns '8.8.8.8'
        option gateway '10.38.140.225'

config interface 'wan'
        option proto 'static'
        option ifname 'eth1'
        option ipaddr '109.69.10.98'
        option netmask '255.255.255.224'
        option gateway '109.69.10.126'

config route
        option interface 'lan'
        option target '10.0.0.0'
        option netmask '255.0.0.0'
        option gateway '10.38.140.225'

config interface 'ttn'
        option proto 'wireguard'
        option private_key 'tBtpfwf65JkCyeuhc47bt87fJRdUKhSBphXLxrKXAM8p'
        option listen_port '45955'
        option mtu '1396'
        list addresses '172.31.0.1/22'

config wireguard_ttn
        option public_key 'u7VjcLp3N2sJ7EcFjsPuRw9pYu6ogRO70NT1eewl+AU='
        option endpoint_port '45955'
        option endpoint_host '10.90.234.5'
        list allowed_ips '172.16.0.0/24'
        list allowed_ips '172.31.0.0/22'

config wireguard_ttn
        option public_key '7JfICIH5zKTSoH/5YT8kMkDmVQdg5Oy2r4PM2PId81c='
        option endpoint_host '10.228.193.115'
        option endpoint_port '45955'
        list allowed_ips '172.16.1.0/24'
        list allowed_ips '172.31.0.0/22'
```

També ens caldrà un protocol d'encaminament dinàmic. Instal·lem OLSR sense cap extensuo o plugin:
```
root@LEDE:~# opkg install olsrd luci-app-olsr
```
La confguració minimalista per tal que funcioni l'anunci de prefixes dins la VPN és:
```
config olsrd             
        option IpVersion '4'
        option FIBMetric 'flat'
        option LinkQualityLevel '2'
        option LinkQualityAlgorithm 'etx_ff'
        option OlsrPort '698'
        option Willingness '3'
        option NatThreshold '1.0'

config LoadPlugin
        option library 'olsrd_arprefresh.so.0.1'
        option ignore '1'

config LoadPlugin
        option library 'olsrd_dyn_gw.so.0.5'
        option ignore '1'

config LoadPlugin
        option library 'olsrd_httpinfo.so.0.1'
        option port '1978'
        list Net '0.0.0.0 0.0.0.0'config InterfaceDefaults

config Hna4
        option netaddr '0.0.0.0'
        option netmask '0.0.0.0'

config LoadPlugin
        option library 'olsrd_jsoninfo.so.0.0'
        option ignore '0'
        option ignore '1'

config LoadPlugin
        option library 'olsrd_nameservice.so.0.3'
        option ignore '1'

config LoadPlugin
        option library 'olsrd_txtinfo.so.0.1'
        option accept '0.0.0.0'
        option ignore '0'

config Interface
        option interface 'ttn'
        option Mode 'ether'
        option ignore '0'
        option Ip4Broadcast '172.31.3.255'
```
