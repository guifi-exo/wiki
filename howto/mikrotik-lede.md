# Support per Mikrotik wAP AC i RB921GS
El 2017 Mikrotik llença al mercat dos productes de gran interés per les xarxes obertes basades en mesh: [RBwAPG-5HacT2HnD](https://lede-project.org/toh/hwdata/mikrotik/mikrotik_rbwapg-5hact2hnd_wap_ac) i [RB921GS-5HPacD-15S](https://lede-project.org/toh/hwdata/mikrotik/mikrotik_rb921gs-5hpacd-15s). Esta tracte de productes basats ens xips wireless IEEE 802.11ac i adaptats tant en preu com en característiques a les necessitats de les xarxes mesh.
A finals de 2017 ja disposem de suport quasi total per OpenWRT/LEDE, gràcies a (https://github.com/rogerpueyo)[rogerpueyo]. De moment en la versió inestable (snapshot).

En aquesta entrada comentarem el procediment de compilació i instal·lació dels binaris en aquests dispositius. Tant aviat com estiguin disponibles les imatges estables compilades, podem passar directament a la secció d'instal·lació des de firmware OEM. L'objectiu és obtenir una imatge genèrica amb LuCI i d'altres eines útils i documentar el procediment de *flash* pel cas particular d'aquests models.

# Compilació d'imatges des de les fonts *snapshot*
Podem seguir les instruccions del projecte (https://lede-project.org/docs/guide-developer/quickstart-build-images)[LEDE] si no tenim el codi font clonat.

# Procediment de *flash*
En general els dispositius de Mikrotik no permeten el flash d'imatges terceres des de la pròpia eina de gestió del fabricant. Tanmateix permet carregar una imatge tipus `vmlinux-initramfs.elf` en RAM i després gravar la imatge a la memòria flash amb `sysupgrade`. Les instruccions genèriques les trobareu a la documentació de (https://wiki.openwrt.org/toh/mikrotik/common)[OpenWRT].
