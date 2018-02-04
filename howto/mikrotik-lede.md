# Support per Mikrotik wAP AC i RB921GS
El 2017 Mikrotik llença al mercat dos productes de gran interés per les xarxes obertes basades en mesh: [RBwAPG-5HacT2HnD](https://lede-project.org/toh/hwdata/mikrotik/mikrotik_rbwapg-5hact2hnd_wap_ac) i [RB921GS-5HPacD-15S](https://lede-project.org/toh/hwdata/mikrotik/mikrotik_rb921gs-5hpacd-15s). Esta tracte de productes basats ens xips wireless IEEE 802.11ac i adaptats tant en preu com en característiques a les necessitats de les xarxes mesh.
A finals de 2017 ja disposem de suport quasi total per OpenWRT/LEDE, gràcies a (https://github.com/rogerpueyo)[rogerpueyo]. De moment en la versió inestable (snapshot).

En aquesta entrada comentarem el procediment de compilació i instal·lació dels binaris en aquests dispositius. Tant aviat com estiguin disponibles les imatges estables compilades, podem passar directament a la secció d'instal·lació des de firmware OEM. L'objectiu és obtenir una imatge genèrica amb LuCI i d'altres eines útils i documentar el procediment de *flash* pel cas particular d'aquests models.

# Compilació d'imatges des de les fonts snapshot
Podem seguir les instruccions del projecte (https://lede-project.org/docs/guide-developer/quickstart-build-images)[LEDE] si no tenim el codi font clonat.

# Procediment de flash
En general els dispositius de Mikrotik no permeten el flash d'imatges terceres des de la pròpia eina de gestió del fabricant. Tanmateix permet carregar una imatge tipus `vmlinux-initramfs.elf` en RAM i després gravar la imatge a la memòria flash amb `sysupgrade`. Les instruccions genèriques les trobareu a la documentació de [OpenWRT](https://wiki.openwrt.org/toh/mikrotik/common).

El primer pas és crear-se en un PC de treball un directori. En el meu cas `/home/user/Development/` i hi depositarem aquestes imatges:
```
loader.sh
openwrt-ar71xx-mikrotik-rb-nor-flash-16M-ac-squashfs-sysupgrade.bin
openwrt-ar71xx-mikrotik-vmlinux-initramfs.elf
```
Caldrà ara instal·lar el servidor DHCP i TFTP. Es recomana el `dnsmasq`. Si treballem amb un Debian o equivalent, només cal instal·lar-lo des dels dipòsits oficials:
```
sudo apt install dnsmasq
```
L'arxiu `loader.sh` és un shell script que activa el `dnsmasq` sobre la interfície de xarxa especificada i lliura l'arxiu especificat per TFTP al dispositiu. He fet una adaptació de l'script original de la documentació [OpenWRT](https://wiki.openwrt.org/toh/mikrotik/common) per tal que permeti configurar la interfície de xarxa i el binari a transferir per la línia d'arguments.
```
#/bin/bash
ip a a 192.168.1.10/24 dev $1
dnsmasq -i $1 --dhcp-range=192.168.1.100,192.168.1.200 \
--dhcp-boot=$2 \
--enable-tftp --tftp-root=/home/user/Development/ -d -u test -p0 -K --log-dhcp --bootp-dynamic
```
Caldrà substituir `user` pel nom d'usuari que tinguem en el directori i `test` per un nom d'usuari disponible en el PC de treball. Normalment és el mateix nom en els dos casos. Fem que l'script sigui executable amb `chmod a+x loader.sh`. En el nostre cas la interfície de xarxa on connectarem el dispositiu és la `enp0s25`. Executem la comanda:
```
./loader.sh enp0s25 openwrt-ar71xx-mikrotik-vmlinux-initramfs.elf
```
Optem per activar el client DHCP en el dispositiu de Mikrotik a través del botó de reset. Connectem el cable de xarxa del dispositiu al PC. Desconnetem l'alimentació i la tornem a connectar mentre premem el botó de reset. El mantenim premut fins que el LED de ETH passa a intermitència ràpida. En aquest moment alliberem el botó de reset i hauríem de veure aquest els missatges de `dnsmasq` que correspon a la trasnferència del binari. Esperems uns segons i ja podem accedir al dispositiu amb ssh:
```
ssh root@192.168.1.1
```
No vindrà amb el password de root configurat. En aquest moment tenim el kernel i el rootfs carregats només en RAM. Per instal·lar-los de manera permanent transferim la imatge _sysupgrade_:
```
scp openwrt-ar71xx-mikrotik-rb-nor-flash-16M-ac-squashfs-sysupgrade.bin root@192.168.1.1:/tmp
```
Accedim per ssh al dispositiu i gravem la imatge a les corresponents particions de la memòria flash:
```
root@lede# sysupgrade -n /tmp/openwrt-ar71xx-mikrotik-rb-nor-flash-16M-ac-squashfs-sysupgrade.bin
```
Esperem uns minuts i ja tindrem el OpenWRT/LEDE instal·lat.
