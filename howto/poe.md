El PoE ens facilita alimentar les antenes de dalt utilitzant el mateix cable de xarxa per on van les dades

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [L'experiència i la intuició ens diu](#lexperi%C3%A8ncia-i-la-intuici%C3%B3-ens-diu)
  - [PoE 24 V](#poe-24-v)
  - [PoE 48 V](#poe-48-v)
- [L'anàlisis i els números ens diuen](#lan%C3%A0lisis-i-els-n%C3%BAmeros-ens-diuen)
  - [Alguns números](#alguns-n%C3%BAmeros)
  - [Fes els teus números!](#fes-els-teus-n%C3%BAmeros)
- [Preguntes freqüents](#preguntes-freq%C3%BCents)
- [Més informació](#m%C3%A9s-informaci%C3%B3)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


# L'experiència i la intuició ens diu

Basat en preguntes que he fet a persones familiaritzades amb el tema, i algunes cerques acreditades o verificades

## PoE 24 V

- fins a 30 m si has de pujar més d'una antena
- fins a 50 m si has de pujar 10 W (potser justet)

## PoE 48 V

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

# L'anàlisis i els números ens diuen

La clau és la [llei d'Omh](https://ca.wikipedia.org/wiki/Llei_d%27Ohm), és a dir la relació entre voltatge (unitats [Volts](https://ca.wikipedia.org/wiki/Volt)), intensitat de corrent elèctric (unitats: [Ampères](https://ca.wikipedia.org/wiki/Ampere)) i resistència `R` (Unitats: [Ohms](https://ca.wikipedia.org/wiki/Ohm) o Ω)

    V = I * R

Un cable llarg es pot considerar una resistència, i la forma de calcular-ho la podeu trobar aquí http://chemandy.com/calculators/round-wire-resistance-calculator.htm 

Calculadora de la pèrdua de voltatge (per veure la diferència de PoE de 24 i 48 V). El cable acostuma de xarxa categoria 5E a ser de 24 AWG

http://www.calculator.net/voltage-drop-calculator.html

Un altre fòrmula que ens pot ser útil és la de [potència elèctrica](https://ca.wikipedia.org/wiki/Pot%C3%A8ncia_el%C3%A8ctrica#Pot.C3.A8ncia_en_corrent_continu):

    P = V * I

## Alguns números

El calculador no és gaire adient per les nostres necessitats (excepte per la dada que ens dóna de 24 AWG en la resistència)

Només cal saber la llargada del cable i la potència elèctrica que necessita cada trasto

En general els trastos consumeixem entre 3W i 6W a 24V per tant els hi cal una corrent entre 125mA i 250mA

Per tal de suportar l'arrancada normalment utilitzo el pijor cas 6W @24V = 250mA

Per tant si creiem que podem aguantar una caiguda de 3V ( és a dir, si alimentem un extrem amb 24V en el altre en tindrem 21V) un trasto de 6W permet tenir un cable de 3V/250mA=12Ω el que fa que puguis tenir un cable de llargada 12Ω/0,08422=142m

Per cada trasto que afegeixis has de dividir aquesta llargada per el nombre de trastos: així una Omnitik UPA amb 4 trastos penjats, o sigui, 5 trastos en total la llargada no pot superar els 142m/5=28,5m

També es pot calcular dient que 5 trastos a 6W cadascun són 30W de consum o sigui 30w/24V=1.25A

3V/1.25A=2.4Ω com a màxim, per tant 2.4Ω/0,08422=28.5m

Si vols fer el càlcul per 48v només hi ha que saber que per 6W la corrent serà la meitat ja que la tensió és el doble: 6W/48v=125mA

Per tant la llargada serà del doble ja que cada trasto necessita la meitat de corrent

A 48v un trasto de 6W pot tenir un cable PoE de 284m

3V/125mA=24Ω el que significa 24Ω/84.22mΩ/m=285m

Es complica si poses un convertidor DC/DC de 48v/24v ja que llavors probablement tens que tenir en compte la eficiéncia del convertidor (aprox entre el 80% i 90%) i la tolerància de la tensió d'entrada

Hi han molts convertidors que treballen de 36v a 52v d'entrada i donen 24v de sortida estables

## Fes els teus números!

Donada tota aquesta informació, ja pots fer els teus números. A més a més, mira de disposar d'algun aparell per mesurar potència elèctrica (W), current (A), voltatge (V), etc. En el meu cas he utilitzat [aquest](http://www.conrad.fr/ce/fr/product/090158/Compteur-de-consommation-Chacon-54355) mesurador d'aparells electrònics a la llar, que em va ajudar molt per tenir els peus a terra.

# Preguntes freqüents

- P: Què vol dir mA?
- R: Vol dir mil·liampères. [Mil·li](https://ca.wikipedia.org/wiki/Mil·li) és un prefix per reduir entre 1000 la quantitat d'una dimensió. mA és tant utilitzat a electricitat com el kg (kilogram) en el dia a dia

- P: Si tinc més corrent (A) la caiguda de tensió o voltatge (V) és menor?
- R: La caiguda de tensió depén del consum de la càrrega. Un PoE de 0.5A 24V pots alimentar una càrrega de 12W i un de 1A una de 24W, per tant no arriba més lluny simplement pot alimentar més coses

# Més informació

https://en.wikipedia.org/wiki/Power_over_Ethernet

els dos estàndards es diuen:

- IEEE 802.3af-2003
- IEEE 802.3at-2009
