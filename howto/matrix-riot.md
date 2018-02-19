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
- [known problems](#known-problems)
  - [notifications](#notifications)
- [todo / extra](#todo--extra)
  - [HTML formatted messages](#html-formatted-messages)
  - [telegram bridge](#telegram-bridge)
  - ["telegram channel" (lista de difusión) in riot/matrix ?](#telegram-channel-lista-de-difusi%C3%B3n-in-riotmatrix-)
  - [captcha](#captcha)
  - [specification for script that migrates user from one server to another](#specification-for-script-that-migrates-user-from-one-server-to-another)
    - [script to blank account in server A](#script-to-blank-account-in-server-a)
  - [use our own integration server](#use-our-own-integration-server)
    - [particular interest: monitoring with prometheus and grafana](#particular-interest-monitoring-with-prometheus-and-grafana)
  - [more bots, bridges](#more-bots-bridges)
- [dark things about matrix and riot](#dark-things-about-matrix-and-riot)

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

matrix-riot homeservers up & running that used this howto:

- https://sevilla.guifi.net/riot
- https://riot.guifi.net
- https://riot.musaik.net

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

password_providers:
 - module: "ldap_auth_provider.LdapAuthProvider"
   config:
     enabled: true
     uri: "ldaps://ldap.guifi.net"
     start_tls: true
     base: "o=webusers,dc=guifi,dc=net"
     attributes:
        uid: "uid"
        mail: "mail"
        name: "uid"

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

# enable communities feature
enable_group_creation: True

EOF
```

[Set up requirements for guifi LDAP](https://github.com/matrix-org/matrix-synapse-ldap3#installation)

    apt-get install python-matrix-synapse-ldap3

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

    apt-get install libpq-dev python-pip python-psycopg2

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

    # good security tips ON - check yours: https://www.ssllabs.com/ssltest/analyze.html?d=matrix.example.com&latest
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    # Ciphers based on the Mozilla SSL Configuration Generator
    ssl_ciphers 'ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA:ECDHE-RSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA256:DHE-RSA-AES256-SHA:ECDHE-ECDSA-DES-CBC3-SHA:ECDHE-RSA-DES-CBC3-SHA:EDH-RSA-DES-CBC3-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:DES-CBC3-SHA:!DSS';
    # run: `openssl dhparam -out /etc/ssl/dhparams2048.pem 2048` src https://weakdh.org/sysadmin.html extra src https://gist.github.com/plentz/6737338
    ssl_dhparam /etc/ssl/dhparams2048.pem;

    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

    ssl_stapling on;
    ssl_stapling_verify on;
    
    ssl_prefer_server_ciphers on;

    # enable session resumption to improve https performance
    # http://vincent.bernat.im/en/blog/2011-ssl-session-reuse-rfc5077.html
    # found here: https://gist.github.com/plentz/6737338
    ssl_session_cache shared:SSL:50m;
    ssl_session_timeout 1d;
    ssl_session_tickets off;

    # good security tips OFF

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

# CHANGE here to use your specific domains
matrix_domain="matrix.example.com"
riot_domain="riot.example.com"
riot_ppath="/var/www/html" # p: parent path
riot_rpath="riot-web" # r: relative path

# thanks MTRNord (@MTRNord:matrix.ffslfl.net)

# ir a ruta de riot estatico
cd "$riot_ppath"

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
        rm -rf "$riot_rpath".bkp
        mv "$riot_rpath" "$riot_rpath".bkp 2> /dev/null
        mkdir "$riot_rpath"
        cd "$riot_rpath"

        echo "New Version found starting download"
        curl -Ls "$download" | tar xz --strip-components=1 -C ./

        # customizations:
        # - delete piwik and change homeserver URL
        # - point to your own homeserver
        # - select a specific welcome static page (if does not exist goes to default)
        jq -M -r 'del(.piwik)' config.sample.json |
          jq -M -r '.default_hs_url = "https://'$matrix_domain'"' |
            jq -M -r '.welcomePageUrl = "https://'$riot_domain'/welcome/matrix.html"' > config.$riot_domain.json

        cd ..
        chown -R www-data:www-data "$riot_rpath"
        echo "$package_id" > "$riot_ppath"/riot_version-id

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

learn more about how data grows https://matrix.org/docs/projects/other/hdd-space-calc-for-synapse.html

## Test federation

To test federation you can use this service: https://matrix.org/federationtester/api/report?server_name=matrix.example.com

or use the source: https://github.com/matrix-org/matrix-federation-tester

# known problems

## notifications

some people do not receive notifications in its smartphone

# todo / extra

## HTML formatted messages

You can send HTML formatted messages (for example for bot/alert notification) with `curl`, at the moment this is [officially not documented](https://github.com/matrix-org/matrix-doc/issues/917)

```
token="check your token access in riot general settings"
room_id="vfFxDRtZSSdspfTSEr" #test:matrix.org
room_server="matrix.org"
homeserver="matrix.org"

curl -XPOST -k -d '{"msgtype":"m.text", "body": "", "format": "org.matrix.custom.html", "formatted_body":"<b>test</b> test <font color =\"red\">red test</font> https://docs.google.com/document/d/1QPncBmMkKOo6\_B2jyBuy5FFSZJrRsq7WU5wgRSzOMho/edit#heading=h.arjuwv7itr4h <table style=\"width:100%\"><tr><th>Firstname</th><th>Lastname</th><th>Age</th></tr><tr><td>Jill</td><td>Smith</td><td>50</td></tr><tr><td>Eve</td><td>Jackson</td><td>94</td></tr></table> https://www.w3schools.com/html/html\_tables.asp"}' "https://matrix.guifi.net:8448/\_matrix/client/r0/rooms/%21$room\_id:$room\_server/send/m.room.message?access\_token=$token"
```

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

implementation: work in progress

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

### script to blank account in server A

```python
#!/usr/bin/env python3

# this script login the specific matrix account and LEAVES ALL ROOMS

# requirements
# - apt install python-pip3
# - pip3 install wheel matrix_client

# based on https://github.com/matrix-org/matrix-python-sdk/blob/master/samples/ChangeDisplayName.py
# useful resource https://github.com/matrix-org/matrix-python-sdk/tree/master/matrix_client

import sys

from matrix_client.client import MatrixClient
from matrix_client.api import MatrixRequestError
from requests.exceptions import MissingSchema

# access data

host="https://matrix.example.com"
username="myuser"
password="mypassword"

# login

client = MatrixClient(host)

try:
    client.login_with_password(username, password)
except MatrixRequestError as e:
    print(e)
    if e.code == 403:
        print("Bad username or password.")
        sys.exit(4)
    else:
        print("Check your server details are correct.")
        sys.exit(2)
except MissingSchema as e:
    print("Bad URL format.")
    print(e)
    sys.exit(3)

# actions

roomlist = client.get_rooms()

print("leaving rooms:")
# list() does a copy of dictionary to avoid error: "RuntimeError: dictionary changed size during iteration" -> src https://stackoverflow.com/questions/11941817/how-to-avoid-runtimeerror-dictionary-changed-size-during-iteration-error
for room in list(roomlist.values()):
    room.leave()
    print("  " + room.room_id + " left")
```

## use our own integration server

- https://dimension.t2bot.io
- https://github.com/turt2live/matrix-dimension

### particular interest: monitoring with prometheus and grafana

- add grafana widget https://github.com/turt2live/matrix-dimension/issues/86
- prometheus alertmanager bot https://github.com/turt2live/matrix-wishlist/issues/28

## more bots, bridges

https://github.com/turt2live/t2bot.io

https://t2bot.io


# dark things about matrix and riot

Political concern: Main funder is AMDOC, search amodoc-mossad on google and you can discover something interesting. The funding situation is changing to have more funders, we will see what happen.

Tecnological concern: matrix generate ALOT ot metadata on the central server, even if the communication is encrypted, the metadata are not and most of the software analysis to generate network maps use just metadata, more you have more the map is accurate

Riot client is not free. Such a hype for a server-client non-free [0] software which tries to act as a Person In The Middle interconnecting any other network...

[0] https://directory.fsf.org/wiki/Talk:Riot-im

