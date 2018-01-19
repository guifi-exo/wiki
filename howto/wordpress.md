# tips

for installation:

https://www.digitalocean.com/community/tutorials/how-to-install-wordpress-on-ubuntu-14-04

hardening (file permissions to user): https://stackoverflow.com/a/23755604

# update wordpress via CLI

## install

as root:

```
curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
php wp-cli.phar --info # check the Phar file to verify that it’s working:
chmod +x wp-cli.phar
mv wp-cli.phar /usr/local/bin/wp
```

src http://wp-cli.org/

## usage

update_wordpress.sh script:

```
#!/bin/bash

cd /var/www/html/wordpress
wp core update
wp plugin update --all
wp theme update --all
cd
```

run it!

```
./update_wordpress.sh 
Success: WordPress is up to date.
Success: Plugin already updated.
```
