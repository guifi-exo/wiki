# Instal·lació del paquet Tunneldigger per LEDE/OpenWRT

Segons la documentació de tunneldigger, cal compilar una imatge de LEDE/OpenWRT per tal d'obtenir el opkg. Recordem els passos bàsics. Clonem el repositori de LEDE:
```
git clone https://git.lede-project.org/source.git lede
```
Això crearà un directori anomenat `lede` on hi tindrem tots els arxius de compilació. Explorem els tags del repositori ja que per defecte el HEAD apunta cap al darrer commit de la versió experimental. Triem la darrera estable:
```
git checkout tags/v17.01.4
```
Segons la documentació de [Tunneldigger](https://github.com/wlanslovenija/tunneldigger), Tunnedigger per LEDE/OpenWRT es troba en el [repositori de la comunitat](https://github.com/wlanslovenija/firmware-packages-opkg). Aquí ens indica que hem d'editar l'arxiu de *feeds* i afegir:
```
src-git nodewatcher https://github.com/wlanslovenija/firmware-packages-opkg.git
```
Tot seguit poden actualitzar i instal·lar els directoris dels paquets dels *feeds*. Triem els paquets de Tunneldigger i d'altres que considerem oportuns amb *Menuconfig*.
```
./scripts/feeds update -a
./scripts/feeds install -a

make menuconfig
```

# Instal·lació del broker
Falta el procés d'instal·lació amb detall...Se suposa que tenim el codi instal·lat a `/srv/tunneldiger`.

Per arrencar manualment:
```
cd /srv/tunneldigger
source /srv/tunneldigger/env_tunneldigger/bin/activate
env_tunneldigger/bin/python -m tunneldigger_broker.main /srv/tunneldigger/broker/l2tp_broker.cfg

```

Per declarar el servei a Debian cal crear un script d'arrancada, per exemple:
```
#!/bin/bash

WDIR=/srv/tunneldigger
VIRTENV_DIR=/srv/tunneldigger
CONF_FILE=l2tp_broker.cfg

cd $WDIR
source $VIRTENV_DIR/env_tunneldigger/bin/activate
env_tunneldigger/bin/python -m tunneldigger_broker.main $WDIR/broker/$CONF_FILE
```
i donem permisos d'execució. Afegim l'arxiu `/etc/systemd/system/tunneldigger.service`:
```
[Unit]
Description = Start tunneldigger L2TPv3 broker
After = network.target

[Service]
ExecStart = /srv/tunneldigger/start-broker.sh

[Install]
WantedBy = multi-user.target
```
Finalment habilitem el nou servei en l'entorn de Debian:
```
systemctl daemon-reload
systemctl enable tunneldigger.service
```
