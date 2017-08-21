# Despliegue sencillo de wifi para un local

Requerimientos: un router con conexión a Internet, y unos cuantos wifi-routers diversos que cada uno tiene por casa

Para evaluar la situación de las diferentes redes wifi usa la aplicación [linssid](https://sourceforge.net/projects/linssid/)

Para cada router:

1. Averiguar cuál es su IP de entrada y sus datos de acceso (más info: adslzone.net o bandaancha.eu), normalmente es http://192.168.1.1
2. El mismo ESSID, por ejemplo guifi.net-CentroSocialLaPalma
3. Contraseña sí, no? Lo mismo para todos
4. Seleccionar diferentes canales wifi libres (cuanto más espacio entre ellos, mejor)
5. Deshabilitar el DHCP, y conectarlos al punto central que da Internet por el conector amarillo, switch (no por el conector de Internet). Esto dificultará el acceso del wifi-router (que habrá que usar direccionamiento estático para acceder), pero de esta forma no interferirá en absoluto con otras redes.

# Utilidades

ver si una tarjeta wifi soporta modo monitor: `iw list | grep monitor`
