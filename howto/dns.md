# DNS de preferència

Enlloc de mirar un DNS com els de proveïdors externs que probablement van molt llunys, potser és més interessant seleccionar un que està ben a prop: a telvent; i que té relació amb fundació guifi.net. Fundació puntcat: `109.69.8.51`. Més informació: http://servidordenoms.cat/

extra: https://wikileaks.org/wiki/Alternative_DNS

# Resolució inversa de DNS

Qui s'encarrega de la resolució inversa d'una IP és el seu propietari o titular. Es pot demanar a aquesta persona o organització (normalment és qui ens ha venut el servei d'Internet) que ens doni una o vàries resolucions inverses concretes (o que hi hagi una resolució genèrica per un rang d'IPs). També es pot demanar delegació de la resolució inversa del DNS està explicada aquí (TODO: extreure com funciona): [RFC2317](http://ietf.org/rfc/rfc2317.txt)

Algú ens ha dit que has de tenir com a mínim un /24 en el cas de IPv4. Confirmem veracitat de la info en el [RFC2317](http://ietf.org/rfc/rfc2317.txt)

Segons [RFC1912](https://www.ietf.org/rfc/rfc1912.txt) hi han serveis (inclòs el sistema dns mateix) que es poden tenir un mal funcionament per una mala resolució inversa

Per tal de fer comprovacions a les vostres IPs utilitzeu l'eina [rdns.py](https://github.com/guifi-exo/doc/blob/master/knowledge/rdns.py)

extra: https://www.dnstree.com/cat/exo/

## ssh

als logs apareix aquest missatge ja que ssh fa moltes comprovacions per verificar qui és qui vol entrar:

`Xxx x xx:xx:xx si sshd[xxxxx]: reverse mapping checking getaddrinfo for xxx-xx-xx-xx-exo.ip4.guifi.net [xxx.xx.xx.xx] failed - POSSIBLE BREAK-IN ATTEMPT!`

## dns

afecta a la reputació del dns, ens ha passat que amb dinahosting, quan poses la IP te la converteix a resolució inversa, i evidentment quan fas consultes intenta fer resolució de la resolució inversa

quan resolució inversa estava malament:
```
dig +trace exo.cat
(...)
dig: couldn't get address for 'xxx-xx-xx-xxx-exo.ip4.guifi.net': no more
```

quan la vam arreglar:
```
dig +trace exo.cat
(...)
;; Received 198 bytes from xxx.xx.xx.xxx#53(xxx-xx-xx-xxx-exo.ip4.guifi.net) in 7 ms

```

## mail

Amb el mail (postfix) m'han dit que mail també (reputació), però no sé exactament com, per què

