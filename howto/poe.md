El PoE ens facilita alimentar les antenes de dalt utilitzant el mateix cable de xarxa per on van les dades

# PoE 24 V

- fins a 30 m si has de pujar més d'una antena
- fins a 50 m si has de pujar 10 W (potser justet)

# PoE 48 V

Aguanta fins a 100 m però requereix d'un equip adicional:

- "solució barata", convertidor 48 a 18 o 24 a dalt
    - si és alguna Ubiquiti compatible (veure el seu manual) es pot utilitzar aquests dos components:
        - [Ubiquiti POE-48-24W](https://dl.ubnt.com/poe48_ds.pdf)
        - [Ubiquiti Instant Power 8023AF Outdoor](https://dl.ubnt.com/datasheets/instant/instant8023af.pdf) o el [model gigabit](https://dl.ubnt.com/datasheets/instant/Instant_802.3af_Gigabit_PoE_Converters_DS.pdf)
    - genèric (requereix caixa estanca): [48 to 24V Gigabit PoE Converter](https://mikrotik.com/product/rbgpoe_con_hp)
- "solució bona", switch de 48 V a dalt. Possibilitats (un o altre):
    - [Ubiquiti Tough Switch-5-POE](https://dl.ubnt.com/datasheets/toughswitch/TOUGHSwitch_PoE_DS.pdf) en caixa estanca
    - [Netonix WS-6-MINI](https://www.netonix.com/ws-6-mini.html) en caixa estanca

nota: un supernode difícilment consumeix més de 50 W

# Preguntes freqüents

- P: Si tinc més corrent (A) la caiguda de tensió o voltatge (V) és menor?
- R: La caiguda de tensió depén del consum de la càrrega. Un PoE de 0.5A 24V pots alimentar una càrrega de 12W i un de 1A una de 24W, per tant no arriba més lluny simplement pot alimentar més coses

# Més informació

La clau es troba en la llei de omh, és a dir la relació entre current, voltatge i resistència

V = I * R

Un cable llarg es pot considerar una resistència, i la forma de calcular-ho la podeu trobar aquí http://chemandy.com/calculators/round-wire-resistance-calculator.htm 

Calculadora de la pèrdua de voltatge (per veure la diferència de PoE de 24 i 48 V). El cable acostuma de xarxa categoria 5E a ser de 24 AWG

http://www.calculator.net/voltage-drop-calculator.html

https://en.wikipedia.org/wiki/Power_over_Ethernet

els dos estàndards es diuen:

- IEEE 802.3af-2003
- IEEE 802.3at-2009

Un altre fòrmula que ens pot ser útil és la potència elèctrica: P = V * I
