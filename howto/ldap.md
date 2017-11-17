test guifi ldap is working (for this example my user is user838)

    ldapsearch -W -H ldaps://ldap.guifi.net -D "uid=user838,o=webusers,dc=guifi,dc=net"
