# tips

for installation: https://www.digitalocean.com/community/tutorials/how-to-install-wordpress-on-ubuntu-14-04

hardening (in a nutshell: don't allow webserver to have access to all files, a potential bad php can harm it all)

    cd /var/www/html
    chown www-data:www-data wordpress
    cd wordpress
    chown www-data:www-data .htaccess
    chown <username>:<username>  -R * # Let your useraccount be owner
    chown www-data:<username> -R wp-content # Let apache be owner of wp-content
    chmod 775 -R wp-content # allow upgrades

recommended plugin: `wordfence`. checks security stuff is set up OK in wordpress

    cd /var/www/html/wordpress/wp-content/plugins
    wget https://downloads.wordpress.org/plugin/wordfence.x.x.x.zip
    unzip wordfence.x.x.x.zip
    chown www-data:user -R wordfence/
    # enable from wp-admin WebGUI

refs used:

- https://stackoverflow.com/questions/28843695/wp-cli-error-installing-plugins-themes-could-not-create-directory-permission
- https://stackoverflow.com/a/23755604

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
wp core language update
cd
```

run it!

```
./update_wordpress.sh 
Success: WordPress is up to date.
Success: Plugin already updated.
```
