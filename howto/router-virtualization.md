# Resultats de proves de diferents SO de routing en Proxmox

Autor: Victor Oncins

S'ha dut a terme proves de validació en el *testbed* d'Espai30 de diferents distribucions de routing. L'objectiu era validar les seves prestacions per tal de dur a terme una migració dels actuals serveis de routing a ITConic. La primera decisió de disseny ha estat la de segmentar el nou sistema de routing en dos o més routers:

* Router d'intercanvi de trànsit d'Internet (ITConic-IX)
* Router comunitari de trànsit de Guifi.net (ITConic-guifi)
* Servidor d'accés de xarxa NAS (ITConic-LNS)

Abans de la migració l'eXO només disposava d'un sol router basat en RouterOS que feia les funcions de router comunitari i de trànsit amb Internet. Aquest plantejament presenta certs inconvenients. Les polítiques de seguretat han de coexistir amb les funcionalitat d'un supernode clàssic de Guifi.net i això complica en certa manera la seva gestió. Un plantejament basat en la segmentació funcional permet especialitzar els rols de cada router i simplificar la seva configuració i gestió.

La infraestructura amb la que es compta és un sistema de cluster de dos nodes Proxmox 4.4 amb un tercer node d'arbitratge per obtenir un sistema HA. En conseqüència cal implementar les solucions de router en un entorn Proxmox (KVM).

L'esquema bàsic de xarxa plantejat és el següent:

```
[FXOLN]<--------------VLAN10 + BGP Peer ----------------->[ITConic-guifi]
[FXOLN]<--VLAN102 + BGP Peer -->[ITConic-IX]<--VLAN95-+-->[ITConic-guifi]
                                                      |
                                                 [ITConic-LNS]
```

L'eXO ha volgut aprofitar el procés de millora per introduir alguna distribució de routing de codi lliure. Es planteja l'ús de VyOS per ITConic-IX. Tanmateix no és possible prescindir de manera senzilla de RouterOS en la part comunitària donat que en aquests moments hi ha túnels EoIP (implementació propietària de RouterOS) amb alguns supernodes.

Segons les proves preliminars fetes en les VM ITConic-IX i ITConic-guifi les distribucions VyOS i RouterOS respectivament resulten força satisfactòries. Les dues VMs fan servir interfícies de xarxa VirtIO oferts per l'hipervisor. Les VMs incorporen drivers per aquestes interfícies que ofereixen un rendiment superior als populars E1000 i Realtek 8139. Segons les proves de rendiment realitzades entre VMs s'aproximen als 10Gbps.
