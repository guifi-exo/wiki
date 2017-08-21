# HTTPS

## Level 0: Automatic

About Level 0: Warning! You trust letsencrypt application too much. You can mitigate that.

I followed: https://certbot.eff.org/all-instructions/#debian-7-wheezy-apache

Suppose we want HTTPS for example.com

```
wget https://dl.eff.org/certbot-auto
chmod a+x certbot-auto
```
certbot-auto accepts the same flags as certbot; it installs all of its own dependencies and updates the client code automatically. So you can just run:

`$ ./certbot-auto`

Tries to install everything automatically, asks what domains you want to have https (I said www.example.com i example.com). Certbot arrived to generate certificates `/etc/letsencrypt/live/example.com/fullchain.pem` but missing http -> https

To do redirection from http to https `# vi /etc/apache2/sites-enabled/default-ssl.conf` (this could be a different file) with:

```
       <IfModule mod_rewrite.c>
               RewriteEngine on
               # Force SSL
               RewriteCond %{HTTPS} off
               RewriteRule (.*) https://%{HTTP_HOST}%{REQUEST_URI}
       </IfModule>
```

and `service apache2 restart`

Cron job `# vi /etc/cron.d/certbot`:
```
# /etc/cron.d/certbot: crontab entries for the certbot package
#
# Upstream recommends attempting renewal twice a day
#
# Eventually, this will be an opportunity to validate certificates
# haven't been revoked, etc.  Renewal will only occur if expiration
# is within 30 days.
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

0 */12 * * * root test -x /home/letsencrypt/certbot-auto && perl -e 'sleep int(rand(3600))' && /home/letsencrypt/certbot-auto renew --quiet --no-self-upgrade
```


Command to check it works: `./certbot-auto renew --dry-run`

## Level 1: No root on certbot

About Level 1: Warning! You trust [x.509 model](https://p.exo.cat/criptica/learning#controversy)

Requirements: nginx and debian 8 jessie

Suposition: `www.example.com`, `example.com` domains

As **root**:
```
echo "deb http://ftp.debian.org/debian jessie-backports main" >> /etc/apt/sources.list

apt-get update && apt-get install certbot -t jessie-backports

adduser letsencrypt --disabled-password --gecos ""
# src http://askubuntu.com/questions/94060/run-adduser-non-interactively/94067#94067

chown letsencrypt:letsencrypt /home/letsencrypt/
mkdir /etc/letsencrypt
chown letsencrypt:letsencrypt /etc/letsencrypt
mkdir /var/lib/letsencrypt
chown letsencrypt:letsencrypt /var/lib/letsencrypt/
mkdir /var/log/letsencrypt
chown letsencrypt:letsencrypt /var/log/letsencrypt/

mkdir /var/www/html/.well-known
chown letsencrypt:letsencrypt -R /var/www/html/.well-known
```

nginx config: `# vi /etc/nginx/sites-enabled/default` at the end put:

```
server {
        listen 80;
        server_name www.example.com example.com;
        
        # new version inspired on this:
        # https://community.letsencrypt.org/t/cannot-renew-certs-when-redirecting-http-to-https/16984/6
        location /.well-known {
                default_type "text/plain";
                allow all;
                root /var/www/html;
        }
        location / {
                return 301 https://example.com$request_uri;
        }
}

server {
        listen 443 ssl;
        ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

        # your stuff HERE!
}
```
And do `service nginx restart`

As **letsencrypt user** (`su letsencrypt` or ssh to letsencrypt user with ssh key) get all certificates in one line:

`certbot certonly --keep --agree-tos --email admin@example.com --webroot -w /var/www/html -d example.com -d www.example.com`

after having HTTPS we can move well-known stuff to HTTPS section (again `# vi /etc/nginx/sites-enabled/default`):

```
server {
        listen 80;
        server_name www.example.com example.com;
        
        return 301 https://example.com$request_uri;
}

server {
        listen 443 ssl;
        ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

        # new version inspired on this:
        # https://community.letsencrypt.org/t/cannot-renew-certs-when-redirecting-http-to-https/16984/6
        location /.well-known {
                default_type "text/plain";
                allow all;
                root /var/www/html;
        }

        # your stuff HERE!
}
```
And do `service nginx restart`

Command to check that still works as **letsencrypt user**: `certbot renew --dry-run`

Cron renewal, should look like this `# vi /etc/cron.d/certbot` (probably you have to change the root to the certbot user):

```
# /etc/cron.d/certbot: crontab entries for the certbot package
#
# Upstream recommends attempting renewal twice a day
#
# Eventually, this will be an opportunity to validate certificates
# haven't been revoked, etc.  Renewal will only occur if expiration
# is within 30 days.
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

0 */12 * * * letsencrypt test -x /usr/bin/certbot && perl -e 'sleep int(rand(3600))' && certbot -q renew
```

Note: If by mistake you run certbot commands with root you probably will need to fix permissions (execute again previous `chown` commands)

extra src https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-16-04

## Level 2: Self-signed

About Level 2: Warning! You are strong, but your solution lacks accessibility for 90% of users

(doubt: is this strong enough?)

Create self-signed certificate in current directory:

`openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ss.key -out ss.crt`

get SHA1 fingerprint:

`openssl x509 -in ss.crt -noout -fingerprint -sha1`

get SHA256 fingerprint:

`openssl x509 -in ss.crt -noout -fingerprint -sha256`

You probably want to put this fingerprint signing it with your GPG key. [Example](https://riseup.net/en/canary)

## Level 3: Plurality of HTTPS

About Level 3: Your site should be accessible with at least two x.509 certificates. One of them should be self-signed. I recommend to use self-signed x.509 for important stuff.

It's easy to have a plurality of certificates with an http reverse proxy (I recommend nginx) using two domains, for example:

- example.com for LetsEncrypt
- ss.example.com for your self-signed certificate

A working example with two different HTTPS. The two HTTPS are linked from [here](https://pep.foundation/source-code/index.html). That link points to:

- [site with CACert](https://cacert.pep.foundation/trac)
- [site with LetsEncrypt](https://letsencrypt.pep.foundation/trac)

### nginx as reverse proxy (example.com)

Note: you will have to point somewhere how you can reach ss.example.com

```
server {
        listen 80;
        server_name example.com www.example.com;

        # force https use
        location / {
                return 301 https://example.com$request_uri;
        }
}

# public site with letsencrypt (le)
server {
        listen 443 ssl;
        server_name example.com www.example.com;

        ssl_certificate /path/to/le.cert;
        ssl_certificate_key /path/to/le.key;

        # uncomment next line if your application requires
        # to upload big files (owncloud, nextcloud, etc.)
        # client_max_body_size 5G;

        location / {
                # how you access your application
                # from the server were nginx is installed
                proxy_pass http://127.0.0.1:8080;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
        }

}

# ss site
server {
        listen 443 ssl;
        server_name ss.example.com;

        ssl_certificate /path/to/ss.cert;
        ssl_certificate_key /path/to/ss.key;

        # uncomment next line if your application requires
        # to upload big files (owncloud, nextcloud, etc.)
        # client_max_body_size 5G;

        location / {
                # suppose your application deeply believes is in http://192.168.1.2:8080
                # you can search and replace this behavior
                subs_filter 'http://192.168.1.2:8080' 'https://192.168.1.2';
                # how you access your application
                # suppose your application is at 192.168.1.2 
                # it could be in the same machine: localhost
                proxy_pass http://192.168.1.2:8080;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
        }
}
```
