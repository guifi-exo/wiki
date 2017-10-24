Drupal sync users with LDAP every day at 01:00

Try authentication via CLI

    apt-get install ldap-utils

Run (change myuser)

    ldapsearch -W -H ldaps://ldap.guifi.net -D "uid=myuser,o=webusers,dc=guifi,dc=net"
