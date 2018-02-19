# Despliegue sencillo de wifi para un local

Requerimientos: un router con conexión a Internet, y unos cuantos wifi-routers diversos que cada uno tiene por casa

Para evaluar la situación de las diferentes redes wifi usa la aplicación [linssid](https://sourceforge.net/projects/linssid/)

Para cada router:

1. Averiguar cuál es su IP de entrada y sus datos de acceso (más info: adslzone.net o bandaancha.eu), normalmente es http://192.168.1.1
2. El mismo ESSID, por ejemplo guifi.net-CentroSocialLaPalma
3. Contraseña sí, no? Lo mismo para todos
4. Seleccionar diferentes canales wifi libres (cuanto más espacio entre ellos, mejor)
5. Deshabilitar el DHCP, y conectarlos al punto central que da Internet por la LAN: uno de los 4 conectores amarillos (puede haber variaciones, no son 4, no son amarillos, ...), pero **no** por el conector a Internet, WAN, Azul. Esto dificultará el acceso al wifi-router pero de esta forma no interferirá en absoluto con otras redes. Cuando nos haga falta acceder a este router en concreto necesitaremos direccionamiento estático para acceder, en GNU/Linux y por consola sería algo así `ip add address 192.168.1.2/24 dev <interfaz>`.

# Utilidades

ver si una tarjeta wifi soporta modo monitor: `iw list | grep monitor`


# Extra

https://wiki.openwrt.org/doc/recipes/dumbap

set 20 MHz for wifi channel https://support.apple.com/es-es/HT202068

legal stuff related to wifi: https://en.wikipedia.org/wiki/List_of_WLAN_channels#5_GHz_(802.11a/h/j/n/ac/ax)
