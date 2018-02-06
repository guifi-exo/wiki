test guifi ldap is working (for this example my user is user838)

    ldapsearch -W -H ldaps://ldap.guifi.net -D "uid=user838,o=webusers,dc=guifi,dc=net"

# ldap for organizations

apt install slapd

https://www.digitalocean.com/community/tutorials/how-to-encrypt-openldap-connections-using-starttls
