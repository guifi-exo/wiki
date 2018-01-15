# Instal·lació del paquet per LEDE/OpenWRT

Segona la documentació de tunneldigger, cal compilar una imatge de LEDE/OpenWRT per tal d'obtenir el opkg. Recordem els passos bàsics:
```
git clone https://git.lede-project.org/source.git lede
```
Explorem els tags del repositori ja que per defecte el HEAD apunta cap al darrer commit de la versió experimental. Triem la darrera estable:
```
git checkout tags/v17.01.4
```
Segons la documentació de [Tunneldigger](https://github.com/wlanslovenija/tunneldigger), Tunnedigger per LEDE/OpenWRT es troba en el [repositori de la comunitat](https://github.com/wlanslovenija/firmware-packages-opkg). Aquí ens indica que hem d'editar l'arxiu de *feeds* i afegir:
```
src-git nodewatcher https://github.com/wlanslovenija/firmware-packages-opkg.git
```
Tot segit poden actualitzar i instal·lar els directoris de paquets dels *feeds*. Triem els paquets de Tunneldigger i d'altres que considerem oportuns amb *Menuconfig*.
```
./scripts/feeds update -a
./scripts/feeds install -a

make menuconfig
```
