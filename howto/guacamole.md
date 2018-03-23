Autor: Josep

# Guacamole

Links de referencia:

- https://guacamole.apache.org/doc/gug/guacamole-docker.html
- https://hub.docker.com/r/guacamole/guacamole/

Calen dos containers i bdd (mysql)

- guacamole/guacd
- guacamole/guacamole

El container guacd s’arranca primer sense cap configuració

A continuació cal crear la bdd.

El container de guacamole inclou un script per crear el fitxer de definicio de la dbb

Per executar-lo:

    run --rm guacamole/guacamole /opt/guacamole/bin/initdb.sh --mysql > initdb.sql


Per crear la bdd es pot seguir el procediment següent:

https://guacamole.apache.org/doc/gug/jdbc-auth.html#jdbc-auth-database-creation

Cal canviar que la bdd estigui disponible en qualsevol adr, tamb el usuari i els permisos d’acces, sobretot si el server te més d’un adaptador

A continuació ja es pot arrancar el container del guacamole


La crida per arrancar-lo es:

    docker run --name guacamole --link guacd:guacd \
        -e MYSQL_HOSTNAME=192.168.1.3  \
    
        -e MYSQL_DATABASE=guacamole_db  \
        -e MYSQL_USER=guacamole_user    \
        -e MYSQL_PASSWORD=el_pass_de_la_bdd \
        -d -p 8080:8080 guacamole/guacamole

Per veure el sistema: 

http://192.168.1.3:8080/guacamole/#/

L'usuari d'acces és: guacadmin guacadmin

Per veure els logs en cas d’error

    docker logs guacamole

    FATAL: No authentication configured


Per accedir al shell

    docker exec -i -t guacamole /bin/bash

Per veure les dades del docker

    docker inspect guacd
