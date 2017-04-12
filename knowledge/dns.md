# DNS de preferència

Enlloc de mirar un DNS com els de proveïdors externs que probablement van molt llunys, potser és més interessant seleccionar un que està ben a prop: a telvent; i que té relació amb fundació guifi.net. Fundació puntcat: `109.69.8.51`. Més informació: http://servidordenoms.cat/

# Resolució inversa de DNSs

Segons [RFC1912](https://www.ietf.org/rfc/rfc1912.txt)

Qui s'encarrega de la resolució inversa del DNS és el titular de les IPs. Es pot demanar al titular que hi hagi una resolució concreta, o es pot demanar delegació de la resolució inversa del DNS està explicada aquí (TODO: extreure com funciona): http://ietf.org/rfc/rfc2317.txt

Algú ens ha dit que has de tenir com a mínim un /24 en el cas de IPv4. Confirmem veracitat de la info en el RFC2317

Hi ha serveis que es poden queixar de una mala resolució inversa:

**ssh**

`Xxx x xx:xx:xx si sshd[xxxxx]: reverse mapping checking getaddrinfo for xxx-xx-xx-xx-exo.ip4.guifi.net [xxx.xx.xx.xx] failed - POSSIBLE BREAK-IN ATTEMPT!`

**dns**

`dig: couldn't get address for 'xxx-xx-xx-xxx-exo.ip4.guifi.net': no more`

**mail** m'han dit que mail també, però no sé exactament com, per què

Per tal de fer comprovacions als vostres rangs, proveu de comprovar-ho amb l'eina [rdns.py](https://github.com/guifi-exo/doc/blob/master/knowledge/rdns.py)

extra: https://www.dnstree.com/cat/exo/
