# On comprar?

Habitualment no et serviran les botigues que pots anar presencial i per tant hauràs de fer la compra per Internet

- [landashop.com](https://www.landashop.com)
- [ciudadwireless.com](https://www.ciudadwireless.com)
- [shop.setup.cat](http://shop.setup.cat/) no HTTPS?

# Barat

Considerem barat quan l'equip costa menys de 100 €

## Equips

Al mercat podreu trobar equips acabats ([CPEs](https://en.wikipedia.org/wiki/Customer-premises_equipment)) que facin la funcionalitat necessària per connectar amb guifi.

Recomanem equips de 5 GHz per evitar interferències, especialment en entorns urbans massius com les ciutats.

- [RB921GS-5HPacD-15S (mANTBox 15s)](https://mikrotik.com/product/RB921GS-5HPacD-15S): un router wifi per a exterior amb ràdio 5 GHz 802.11ac i antena sectorial de 120º integrada. [Commit openwrt](https://github.com/openwrt/openwrt/commit/82626cc145610b8b6485d650693629ef0b943505)
- [RBwAPG-5HacT2HnD (wAP AC)](https://mikrotik.com/product/RBwAPG-5HacT2HnD): un router wifi per a interior/exterior amb ràdios 2.4 GHz 802.11n 2:·2 i 5 GHz 802.11ac 3:3 omnidireccionals. [Commit openwrt](https://github.com/openwrt/openwrt/commit/e15c63a37574bd15ce3a6636c2f04741ab76f7b9#diff-a8a8fafd47b7c67a2dd5176236f2ef61)
- [Ubiquiti Nanostation M5](https://dl.ubnt.com/datasheets/nanostationm/nsm_ds_web.pdf) sèrie XM (antiga) o XW (nova): Tenen tota la funcionalitat
- [Alfa Network N5](http://www.alfa.com.tw/products_show.php?pc=127&ps=103): alternativa a Nanostation M5. Contra, no es pot treure el PoE passthrough del port WAN. S'ha d'accedir via serial. La "versió 1" està afectada per problemes de capacitat (que la imatge no cap, i que té [32 MB de RAM](https://lede-project.org/meta/infobox/432_warning))
- ~~Ubiquiti Nanostation 5~~: És un model massa antic, no funcionarà amb mesh/qMp
- ~~Ubiquiti Nanostation Loco M5~~: No la recomanem, molta gent ha tingut males experiències amb elles, té mala qualitat, pot tenir comportament no esperat.

## Switch

- ?

## Routers

Si vols instal·lar OpenWrt o LEDE que tinguin més de 4 MB de flash i 32 MB de RAM

- En general:
    - tp-link
    - ubiquiti
    - https://www.gl-inet.com/
- routers de la estètica (assegurar-se consultant les wikis de OpenWrt i LEDE):
    - https://wiki.openwrt.org/toh/tp-link/tl-wr1043nd
    - https://wiki.openwrt.org/toh/tp-link/tl-wdr4300
- Router "debian" edgeos: https://www.landashop.com/ubiquiti-networks-edge-routerx-sfp-eu.html
- Routers amb SIM 4G
    - TP-Link TL-MR6400
    - TP-Link MR-200

# Car

Considerem car quan l'equip costa 100 € o més

- Ubiquiti Rocket M5 sèrie XM (antiga) o XW (nova): Tenen tota la funcionalitat. Costa menys de 100 € però requereix de la compra d'un equipament adicional (antena) per al seu funcionament:
    - Dish (plat): ...
    - Sectorial: ...
