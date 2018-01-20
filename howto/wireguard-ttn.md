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
