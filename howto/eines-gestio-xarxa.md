# Bàsiques

xarxa 

- ping [CLI] - comprova disponibilitat i latència punt a punt

- mtr [CLI] - comprova disponibilitat i latència de tot el camí

- ssh [CLI] - accés remot

- nmap [CLI] - comprova estat dels ports a l'objectiu

Wifi

- Linsid [GUI] - [comprova interferències del wifi](https://a.fsdn.com/con/app/proj/linssid/screenshots/channels.jpg/1)

# Monitors

- cacti [WebGUI] - gràfiques sobre SNMP

- nagios [WebGUI] - alertes

# Configuradors

- ansible [CLI] i semaphore [WebGUI]

# Misc - Scripts

## Canvi de canal massiu a una xarxa qMp

Autor: Llorenç

```bash
#!/bin/sh

dir="/etc/config"
from="124"
to="132"

for f in "wireless" "qmp"
do
    f="$dir/$f"
    if [ ! -f "$f" ] ; then
	echo "$f?"
	exit 1
    fi
    echo "canviant $f"
    mv $f ${f}.back
    cat ${f}.back | sed "s/\(channel  *.\)$from/\1$to/" > $f
    echo "Fitxers: $f, ${f}.back"
done

```
