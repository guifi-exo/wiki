Es muy probable que hasta que no esté 100% en markdown (y revisado) se vea mejor así: https://raw.githubusercontent.com/guifi-exo/doc/master/knowledge/chat.md

# matrix

- Backend: Matrix (identidades y datos).
- Características: Granularidad de los permisos, genérico y por sala
- Frontend (visualización):
    - Matrix angular client (simple) http://chat.hackmeeting:8008
    - Riot.im http://chat.hackmeeting.tgz
    - Cliente Android. Enlace apk riot.im: https://f-droid.org/repository/browse/?fdfilter=riot&fdid=im.vector.alpha
- Federación parecida a correo electrónico.
- Ejemplo desde guifi.net: chat local, que se conecta con otros chat locales y/o internet
- Hace bridge con IRC, XMPP (?), Telegram, Rocketchat, etc.

```
sintaxis:
    @ usuario:servidor
    # canal:servidor
    nota: a veces es opcional poner servidor (no lo tenemos claro :D)
```

instalación (leer más abajo para más detalles):
- ponemos matrix con cliente angular simple
- si queremos un buen cliente, ponemos apache2 con ficheros estáticos del riot.im
- si DNS configurar SRV para que federe Matrix

si quieres HTTPS configurar certificado letsencrypt

## Chat para Hackmeeting y organizaciones

links iniciales:
- https://matrix.org
- https://matrix.org/docs/guides/faq.html
- https://xo.tc/seting-up-matrix-synapse-and-riot-on-debian-8-jessie.html
server hemos puesto: chat.hackmeeting.tgz
https://dockr.eurogiciel.fr/blogs/embedded/matrix-debian/
Este segundo enlace nos ha permitido corregir el error que teníamos con el primer enlace.
Faltaba cambiar una línia de codigo en el fichero del arranque del servicio
/etc/init.d/matrix-synapse
de tener 
`chown $USER:nogroup $PIDFILE`
hemos puesto
`chown $USER:nogroup $PIDFILE /var/lib/$NAME/media`
también ha sido necesario quitar las comas al final de las línias del fichero
`/etc/matrix-synapse/conf.d/webclient.yaml`
I cambiar el fichero de configuración para habilitar el webclient.

Cliente por defecto
`http://chat.hackmeeting.tgz:8008`

## BASE DE DATOS

Por defecto utiliza sqlite3 y el fichero apunta a:

database: "/var/lib/matrix-synapse/homeserver.db"
podemos utilizar Postgres para mejorar el rendimiento y mejorar la seguridad de los backups

https://github.com/matrix-org/synapse/blob/master/docs/postgres.rst

## CLIENTE WEB

cambiar servidores por defecto; haciéndolo fácil

cp config.sample.json config.json
en config.json cambiar las lineas
    "default_hs_url": "https://matrix.org",
    "default_is_url": "https://vector.im",
    por
    "default_hs_url": "https://chat.hackmeeting.tgz:8448",
    "default_is_url": "https://chat.hackmeting.tgz",
más detalles https://github.com/vector-im/vector-web#configjson

si tienes un HTTPS self signed tienes que aceptar el certificado del homeserver matrix
siguiente paso: vamos a probar a quitar el HTTPS

Si queremos quitar el https, simplemente cambiamos en el archivo de configuracion 
  "default_hs_url": "http://192.168.10.19:8008",
 
Para permitir usuarios invitados, cambiar
allow_guest_access: True

## BRIDGE CLIENTE IRC

apt-get install curl

not tested:
To install all dependencies and add a binary matrix-appservice-irc:
 $ npm install matrix-appservice-irc --global
src https://github.com/matrix-org/matrix-appservice-irc
dominio



## Extras

notas sueltas:
apt-get install python-pip
pip install --upgrade --force "pyopenssl>=0.14"
pip install setuptools_ext

instrucciones testing pedro:
lxc-create -n matrix -t debian -- -r jessie
lxc-start -n matrix -d
lxc-attach -n matrix
apt-get install wget


Instalar cliente vector
apt-get install apache2
wget https://vector.im/packages/vector-v0.8.3.tar.gz
tar xvf vector-v0.8.3.tar.gz
mv vector-v0.8.3.tar.gz /var/www/html/vector
chown www-data:www-data /var/www/html/vector

Extra:
Docker container para probar (se lanza en 2 pasos):
    https://hub.docker.com/r/silviof/docker-matrix/

Detalles:
/var/lib/matrix-synapse/homeserver.db (SQLITE con los datos como imágenes, texto)

user vdo ====> @vdo:gulik.greyfaze.net

 ** Entrar en Freenode desde Matrix:
    #freenode_#channelname:matrix.org


Extra: Matrix riot desde tor, así no nos preocupamos de ip's ni dominios




script para instalar
====================

```
sudo apt-get install matrix-synapse-angular-client 

sudo cp -av /etc/matrix-synapse/conf.d/webclient.yaml /etc/matrix-synapse/conf.d/webclient.yaml.orig

sudo sed -e 's|,$||g' -i /etc/matrix-synapse/conf.d/webclient.yaml

sudo cp -av  /etc/init.d/matrix-synapse   /etc/init.d/matrix-synapse.orig

sudo sed -e 's|chown $USER:nogroup $PIDFILE.*|chown $USER:nogroup $PIDFILE /var/lib/$NAME/media|g' -i /etc/init.d/matrix-synapse

diff -u /etc/init.d/matrix-synapse.orig    /etc/init.d/matrix-synapse

sudo cp -av /etc/matrix-synapse/homeserver.yaml /etc/matrix-synapse/homeserver.yaml.orig

sudo sed -i 's|enable_registration: False|enable_registration: True|g' -i /etc/matrix-synapse/homeserver.yaml

#rm -f /etc/matrix-synapse/conf.d/*.orig /etc/matrix-synapse/conf.d/*~

sudo /etc/init.d/matrix-synapse restart
```

Instalación mediante virtualenv partiendo de Debian 8 básico
============================================================

* Primero satisfacemos las dependencias necesarias:

```
sudo apt-get install build-essential python2.7-dev libffi-dev \
                     python-pip python-setuptools sqlite3 \
                     libssl-dev python-virtualenv libjpeg-dev libxslt1-dev
```

* Vamos a instalar en homeserver con usuario no privilegiado del sistema:

```
virtualenv -p python2.7 ~/.synapse
source ~/.synapse/bin/activate
pip install --upgrade setuptools
pip install https://github.com/matrix-org/synapse/tarball/master

```

* Ahora creamos los archivos de configuración (sustituye tu dominio)

```
python -m synapse.app.homeserver \
    --server-name sevilla.guifi.net \
    --config-path homeserver.yaml \
    --generate-config \
    --report-stats=yes

```

* Finalmente vamos a crear el primer usuario del sistema

```
source ~/.synapse/bin/activate
synctl start # if not already running
register_new_matrix_user -c homeserver.yaml https://localhost:8448
New user localpart: Usuario1
Password:
Confirm password:
Success!
```

pruebas de federación
=====================

$ cpan App::MatrixTool
$ matrixtool server-key your.server.name.here

$ matrixtool notary your.server.name.here matrix.org

src https://github.com/matrix-org/synapse/issues/1142

federation: SRV records

doc federation
==============

https://github.com/matrix-org/synapse#setting-up-federation

error de federación
===============
InvalidAddressError: write() only accepts IP addresses, not hostnames

