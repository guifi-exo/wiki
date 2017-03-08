Instal·lació

# Comanda útil per valorar qualitat del wifi en context d'instal·lació

`while true; do clear; iw dev wlan0 station dump; sleep 1; done`

Vagi a la subsecció: Més sobre la comanda, per a més informació.

Cada segon obtindrem la següent sortida, pot veure-la a la subsección: Sortida de la comanda.

Resulta útil per 2 escenaris que formen part de l'instal·lació guifi d'un node:

- Alineament de l'antena: Consisteix a moure l'antena del node de guifi per tal d'obtindre el millor enllaç possible. Amb el mètode típic des de qMp s'ha d'esperar 5 seguns aproximadament, i no aconseguíem, per exemple, millor de -81 dBm. Amb aquest mètode vam poder afinar fins -74 dBm. També és una forma de controllar l'equilibri entre el RX i TX (recepció i transmissió). Estic parlant especialment pel cas d'un node precari: és un node el qual no té visibilitat directa, però es beneficia dels rebots.
- Prova de cobertura del punt d'accés a l'espai. La mateixa comanda en l'ordinador portàtil (si tenim GNU/Linux) i en moviment, ens permetrà verificar àgilment la qualitat de la cobertura del punt d'accés wifi a l'espai en qüestió. I podrem verificar quin és el millor lloc per posar el punt d'accés wifi o si en calen més.

## Més sobre la comanda

escrit de forma clara:

```
while true; do
    clear
    iw dev wlan0 station dump
    sleep 1
done
```

while és una estructura de control que executa un codi donada una condición. En aquest cas la condició sempre serà certa, per tant, s'executarà indefinidament fins que es pari manualment (Control+C).

I què executa? Per començar `clear` neteja la pantalla. Després la comanda `iw dev wlan0 station dump` ens dona informació rellevant sobre com estem associats. Segueix `sleep 1` com a pausa per executar la comanda cada segon. `done` posa fi a l'estructura de control.

## Sortida de la comanda

```
Station 12:34:56:78:9a:bc (on wlan0)
    inactive time: 60 ms
    rx bytes: 25495350
    rx packets: 109678
    tx bytes: 1535773
    tx packets: 10623
    tx retries: 10359
    tx failed: 0
    signal:   -77 dBm
    signal avg: -76 dBm
    tx bitrate: 26.0 MBit/s MCS 3
    rx bitrate: 43.3 MBit/s MCS 4 short GI
    authorized: yes
    authenticated: yes
    preamble: long
    WMM/WME: yes
    MFP: no
    TDLS peer: no
```
