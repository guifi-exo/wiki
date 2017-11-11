<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [Presentation](#presentation)
- [Install on Debian 9 stretch 2017-10-06](#install-on-debian-9-stretch-2017-10-06)
  - [First steps](#first-steps)
  - [DNS configuration](#dns-configuration)
  - [Accessibility to the server](#accessibility-to-the-server)
    - [reverse proxy server with nginx](#reverse-proxy-server-with-nginx)
    - [web static client](#web-static-client)
      - [script to upgrade static riot](#script-to-upgrade-static-riot)
  - [Data](#data)
  - [Test federation](#test-federation)
- [Instalación desde el código fuente y con virtualenv partiendo de Debian 8 básico - sevillaguifi](#instalaci%C3%B3n-desde-el-c%C3%B3digo-fuente-y-con-virtualenv-partiendo-de-debian-8-b%C3%A1sico---sevillaguifi)
- [known problems](#known-problems)
  - [notifications](#notifications)
- [todo / extra](#todo--extra)
  - [telegram bridge](#telegram-bridge)
  - [telegram channel in riot/matrix ?](#telegram-channel-in-riotmatrix-)
  - [captcha](#captcha)
  - [specification for script that migrates user from one server to another](#specification-for-script-that-migrates-user-from-one-server-to-another)
  - [use our own integration server](#use-our-own-integration-server)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Presentation

- [Matrix](https://matrix.org/) server: now [synapse](https://github.com/matrix-org/synapse), comming soon [dendrite](https://github.com/matrix-org/dendrite)
- [How it works?](https://matrix.org/#about)
- [Status of the project](https://matrix.org/blog/2017/07/07/a-call-to-arms-supporting-matrix/). [Extra](https://matrix.org/blog/2017/07/19/status-update/)
- Based on #channels, and @people attached to them. Its access: Guest (Read-only, Read + Write), Login (Local OR LDAP), Encrypted channels through Double [Ratchet algorithm](https://en.wikipedia.org/wiki/Double_Ratchet_Algorithm) - device based encryption (encrypted-devices.png). History control (no, public, semipublic, private)
    - `@user:<server>, #channel:<server>`
    - public channels
        - Who can access this room?
        - Anyone who knows the room's link, including guests
        - List this room <domain>'s room directory?

- Clients:
    - [There are a lot](https://matrix.org/docs/projects/try-matrix-now.html)
    - Recommended: riot.im/app HTML5 App, Desktop (Electron), AppStore, Google Play, F-Droid
        - Custom server config (login-riot-guifi.png)
        - Room directory (public channels)
        - Start chat
- Bridge with other networks. [Thought](https://xkcd.com/1810/), [response from Matrix](https://twitter.com/matrixdotorg/status/841424770025545730)
- Riot Integrations: IRC networks (TODO: upload integrations-irc.png), jitsi (TODO: upload jitsi.png), [more](https://medium.com/@RiotChat/riot-im-web-0-12-7c4ea84b180a)
- Locations: Spanish 79%, Catalan 0%

# Install on Debian 9 stretch 2017-10-06

This guide helps you to install a matrix server using authentication of a particular LDAP (guifi.net) with a postgresql database. Hope it helps you to be inspired on your particular needs.

## First steps

Run all following commands as root user

Add repository

```
cat <<EOF > /etc/apt/sources.list.d/synapse.list
deb http://matrix.org/packages/debian/ stretch main
deb-src http://matrix.org/packages/debian/ stretch main
EOF
```

Add repo key

    curl -s https://matrix.org/packages/debian/repo-key.asc | apt-key add -

Install synapse matrix server

    apt-get install matrix-synapse

The two asked options are stored here:

- /etc/matrix-synapse/conf.d/report_stats.yaml
- /etc/matrix-synapse/conf.d/server_name.yaml

Config at `/etc/matrix-synapse/homeserver.yaml` is overridden by config in `/etc/matrix-synapse/conf.d`. Let's add all stuff at `/etc/matrix-synapse/conf.d/guifi.yaml`:

```
cat <<EOF > /etc/matrix-synapse/conf.d/guifi.yaml
# overridden: default is sqlite
database:
  name: psycopg2
  args:
    user: synapse_user
    password: synapse_user
    database: synapse
    host: localhost
    cp_min: 5
    cp_max: 10

# LDAP from guifi
ldap_config:
  enabled: true
  uri: "ldaps://ldap.guifi.net"
  base: "o=webusers,dc=guifi,dc=net"
  attributes:
    uid: "uid"
    mail: "mail"
    name: "cn"

# overridden: default is false
allow_guest_access: True

# reverse proxy -> https://github.com/matrix-org/synapse#using-a-reverse-proxy-with-synapse
# just adds on port 8008:
#  + bind_addresses: ['127.0.0.1']
#  + x_forwarded: true

listeners:
  # Main HTTPS listener
  # For when matrix traffic is sent directly to synapse.
  -
    # The port to listen for HTTPS requests on.
    port: 8448

    # Local interface to listen on.
    # The empty string will cause synapse to listen on all interfaces.
    #bind_address: ''
    # includes IPv6 -> src https://github.com/matrix-org/synapse/issues/1886
    bind_address: '::'

    # This is a 'http' listener, allows us to specify 'resources'.
    type: http

    tls: true

    # Use the X-Forwarded-For (XFF) header as the client IP and not the
    # actual client IP.
    x_forwarded: false

    # List of HTTP resources to serve on this listener.
    resources:
      -
        # List of resources to host on this listener.
        names:
          - client     # The client-server APIs, both v1 and v2
          - webclient  # The bundled webclient.

        # Should synapse compress HTTP responses to clients that support it?
        # This should be disabled if running synapse behind a load balancer
        # that can do automatic compression.
        compress: true

      - names: [federation]  # Federation APIs
        compress: false

  # Unsecure HTTP listener,
  # For when matrix traffic passes through loadbalancer that unwraps TLS.
  - port: 8008
    tls: false
    bind_address: '127.0.0.1'
    type: http

    x_forwarded: true

    resources:
      - names: [client, webclient]
        compress: true
      - names: [federation]
        compress: false

EOF
```

[Set up requirements for guifi LDAP](https://github.com/matrix-org/matrix-synapse-ldap3#installation)

    pip install matrix-synapse-ldap3

[Set up requirements](https://wiki.debian.org/PostgreSql#Installation)

    apt-get install postgresql

create user

    su -s /bin/bash postgres -c "createuser synapse_user"

[enter postresql CLI](https://wiki.debian.org/PostgreSql#User_access):

    su -s /bin/bash postgres -c psql

[put password to user](https://stackoverflow.com/questions/12720967/how-to-change-postgresql-user-password)

    ALTER USER "synapse_user" WITH PASSWORD 'synapse_user';

and [set up database](https://github.com/matrix-org/synapse/blob/master/docs/postgres.rst#set-up-database)

    CREATE DATABASE synapse
     ENCODING 'UTF8'
     LC_COLLATE='C'
     LC_CTYPE='C'
     template=template0
     OWNER synapse_user;


[Set up client in Debian/Ubuntu](https://github.com/matrix-org/synapse/blob/master/docs/postgres.rst#set-up-client-in-debianubuntu)

    apt-get install libpq-dev python-pip
    pip install psycopg2

note: [synapse currently assumes python 2.7 by default](https://github.com/matrix-org/synapse#archlinux)

Start or restart matrix service

    service matrix-synapse restart

To check if is running:

    service matrix-synapse status

## DNS configuration

This DNS configuration is required to see federation working in your matrix server

[More info setting up federation](https://github.com/matrix-org/synapse#setting-up-federation) 

    matrix.example.com IN A <IP>
    riot.example.com IN A <IP>
    _matrix._tcp.example.com. 3600 IN SRV 10 0 8448 matrix.example.com.

## Accessibility to the server

Requirements:

    apt-get install certbot nginx-full

### reverse proxy server with nginx

```
matrix_domain="matrix.example.com"
cat <<EOF > /etc/nginx/sites-available/${matrix_domain}
server {
    listen 80;
    listen [::]:80;
    server_name ${matrix_domain};

    location /.well-known {
            default_type "text/plain";
            allow all;
            root /var/www/html;
    }

    return 301 https://\$host\$request_uri;
}

server {
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name ${matrix_domain};

    ssl_certificate /etc/letsencrypt/live/${matrix_domain}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/${matrix_domain}/privkey.pem;

    # static front page to anounce how works the service
    # example: https://github.com/guifi-exo/public/tree/master/web/matrix.guifi.net
    location / {
        root /var/www/html;
        try_files /matrix.html /matrix.html;
    }

    location /_matrix {
        proxy_pass http://127.0.0.1:8008;
        proxy_set_header X-Forwarded-For $remote_addr;
    }
}
EOF

ln -s /etc/nginx/sites-available/${matrix_domain}.conf /etc/nginx/sites-enabled/${matrix_domain}.conf
certbot certonly -n --keep --agree-tos --email ${matrix_email} --webroot -w /var/www/html/ -d ${matrix_domain}
service nginx reload
```

### web static client

```
riot_domain="riot.example.com"
riot_email="info@example.com"
cat <<EOF > /etc/nginx/sites-available/${riot_domain}.conf
server {
    listen 80;
    listen [::]:80;
    server_name ${riot_domain};

    location /.well-known {
            default_type "text/plain";
            allow all;
            root /var/www/html;
    }

    return 301 https://\$host\$request_uri;
}

server {
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name ${riot_domain};

    ssl_certificate /etc/letsencrypt/live/${riot_domain}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/${riot_domain}/privkey.pem;

    # static front page to anounce how works the service (inside riot)
    # example: https://github.com/guifi-exo/public/tree/master/web/riot.guifi.net
    location /welcome {
        alias /var/www/html/riot.guifi.net;
        index /matrix.html;
    }
    location /fp-img {
        alias /var/www/html/riot.guifi.net/fp-img;
    }

    root /var/www/html/riot-web;
}
EOF

ln -s /etc/nginx/sites-available/${riot_domain}.conf /etc/nginx/sites-enabled/${riot_domain}.conf

certbot certonly -n --keep --agree-tos --email ${riot_email} --webroot -w /var/www/html/ -d ${riot_domain}

service nginx reload
```

#### script to upgrade static riot

Requirements:

    apt-get install jq

edit file `vi /usr/local/bin/update-riot.sh`, add following content:

```
#!/bin/bash

# thanks MTRNord (@MTRNord:matrix.ffslfl.net)

# ir a ruta de riot estatico
cd /var/www/html

content=$(curl -s https://api.github.com/repos/vector-im/riot-web/releases/latest)
package_id=$(jq -r '.id' <<< "$content")

if [ "$package_id" != "$(cat ./riot_version-id 2> /dev/null )" ]
  then
    assets=$(jq -r '.assets' <<< "$content")
    download_asset=$(jq -r '.[0]' <<< "$assets")
    content_type=$(jq -r '.content_type' <<< "$download_asset")
    if [ "$content_type" == "application/x-gzip" ]
      then
        download=$(jq -r '.browser_download_url' <<< "$download_asset")

        #cd /var/www
        rm -rf riot-web.bkp
        mv riot-web riot-web.bkp 2> /dev/null
        mkdir riot-web
        cd riot-web

        echo "New Version found starting download"
        curl -Ls "$download" | tar xz --strip-components=1 -C ./

        # customizations:
        # - delete piwik and change homeserver URL
        # - point to your own homeserver
        # - select a specific welcome static page
        jq -M -r 'del(.piwik)' config.sample.json |
          jq -M -r '.default_hs_url = "https://matrix.example.com"' |
            jq -M -r '.welcomePageUrl = "https://riot.example.com/welcome/matrix.html"' > config.riot.example.com.json

        cd ..
        chown -R www-data:www-data riot-web
        echo "$package_id" > /var/www/html/riot_version-id

      else
        echo "Found a new version but first download link doesn't match needed file format"
    fi

  else
    echo "Already latest version"
fi
```

edit file `vi /etc/cron.d/updateriot`, add following content:

```
SHELL=/bin/bash

40 6 * * * root /usr/local/bin/update-riot.sh
```

This script breaks if the gzip file isn't at the first position, TODO: be inspired in this improved (not reviewed) version: https://github.com/grigruss/Riot-web-server-update/blob/master/riot-update.sh

## Data

Data grows here:

- `/var/lib/postgresql`
- `/var/lib/matrix-synapse/media`
- `/var/log/matrix-synapse/` - warning, uses up to 1 GB, change behavior in `/etc/matrix-synapse/log.yaml`

I symlink this directories to specific volume

## Test federation

To test federation you can use this service: https://matrix.org/federationtester/api/report?server_name=matrix.example.com

or use the source: https://github.com/matrix-org/matrix-federation-tester

# Instalación desde el código fuente y con virtualenv partiendo de Debian 8 básico - sevillaguifi

* Primero satisfacemos las dependencias necesarias:

```
sudo apt-get install build-essential python2.7-dev libffi-dev \
                     python-pip python-setuptools sqlite3 \
                     libssl-dev python-virtualenv libjpeg-dev libxslt1-dev
```

* Vamos a instalar el homeserver con un usuario no privilegiado del sistema:

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

* Finalmente crearemos el primer usuario del sistema

```
source ~/.synapse/bin/activate
synctl start # if not already running
register_new_matrix_user -c homeserver.yaml https://localhost:8448
New user localpart: Usuario1
Password:
Confirm password:
Success!
```

* Para arrancar el homeserver introducimos estos comandos

```
cd ~/.synapse
source ./bin/activate
synctl start 
```


# known problems

## notifications

some people do not receive notifications in its smartphone

# todo / extra

## telegram bridge

https://github.com/SijmenSchoon/telematrix

https://t2bot.io/telegram/

https://medium.com/@mujeebcpy/bridging-of-riot-and-telegram-cccb16a955f1

Comment about telegram bridge: A matrix els usuaris de telegram es veuen com un usuari de matrix, però els missatges escrits a matrix a telegram els diu un bot que diu "tal persona a dit"

## "telegram channel" (lista de difusión) in riot/matrix ?

Only some people can send messages, and lots of listeners

https://telegram.org/faq_channels#q-what-39s-a-channel

Solution? You can restrict users from sending messages to the room and only accept Moderator, Admin, etc. The rule has the name "To send messages, you must be a" 

## captcha

https://github.com/matrix-org/synapse/blob/master/docs/CAPTCHA_SETUP.rst

## specification for script that migrates user from one server to another

TODO: implement

ingredients:

- matrix API
- userA_A: user A in server matrix.a.com
- userA_B: user A in server matrix.b.com

objective: perform migration from userA_A to userA_B

procedure:

- userA_A massively invites userA_B to all its rooms
- userA_B massively accepts invitations of userA_A
- userA_A puts the same permissions it has on userA_B
- export riot encryption keys from userA_A to file
- import riot encryption keys from file to userA_B
- [optional: blank account in server A] userA_A leaves all rooms she is in

## use our own integration server

- https://dimension.t2bot.io
- https://github.com/turt2live/matrix-dimension

### particular interest: monitoring with prometheus and grafana

- add grafana widget https://github.com/turt2live/matrix-dimension/issues/86
- prometheus alertmanager bot https://github.com/turt2live/matrix-wishlist/issues/28

## more bots, bridges

https://github.com/turt2live/t2bot.io

https://t2bot.io
