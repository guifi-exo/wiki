### ¿Qué hardware necesito como mínimo para comenzar?


### ¿Necesito una antena y un router?
Depende de la proyección que quieras para tu punto de acceso:

* **¿Unicamente quieres conectarte tú?**  Necesitas ....
* **¿Quieres que se conecte toda tu comunidad de vecinos?** Necesitas ....
* **¿Quieres poder facilitar el acceso a la red guifi a toda tu zona?**  Necesitas .... 

### ¿Qué equipo/marca es el/la más recomendable para comenzar?

### ¿A dónde me tengo que conectar?

Tu nodo debe conectarse a un SN o Super-Nodo y tus dispositivos se conectarán a tu nodo mediante un AP.

### ¿Que es un Nodo?

Un nodo es el punto de conexión final de la red al que se le pueden conectar diferentes equipos para dar diferentes servicios. 
Por ejemplo: tu antena y router forman un nodo, tu conectas a la wifi que da ese router / AP o mediente cable de red. Además puedes conectar un servidor donde alojar una página web.

### ¿Que es un Super-Nodo?

Un SN o Super-Nodo es un nodo dedicado ampliar la rama principal de la red guifi. Requiere una instalación y configuración mas amplia ya que su enlace debe ser mucho mas estable que un nodo.

### ¿Que es un AP?

AP es la abreviatura de "Access Point" en inglés o "Punto de acceso" en Español. Se hace referencia al punto de acceso que se utiliza para conectar los diferentes dispositivos finales (Móvil, tablet, Ordenador, etc)

### ¿Qué significan los puntos y estrellas del mapa de conexión?

Para empezar, decir que el mapa actual solo refleja las conexiones de tipo o modo infraestructura, es decir, conexiones entre supernodos a través de protocolos de enrutamiento BGP o OSPF, y de relación entre punto de acceso y estación. Otras tecnologías como la mesh, no se visualizan bien.

Los colores significan:

* Línea Azul: Enlace proyectado (pendiente)
* Línea Naranja: Enlace en pruebas (si funciona bien por un tiempo pasará a amarillo o verde)
* Línea Amarillo: Enlace de acceso a un cliente (nodo cliente conecta a supernodo), no extiende red
* Línea Verde: Enlace troncal, entre supernodos, enlace que extiende la red
* Punto Rojo: nodo mesh, los nodos mesh se está investigando mejoras de su visualización, se ven mejor aquí: http://sants.guifi.net/maps/ y http://libremap.net/

Los simbolos significan:

* Puntos: nodo, ubicación geográfica donde hay una instalación de telecomunicaciones guifi
* Lineas: conexiones entre nodos guifi (los puntos), pueden ser wifi, fibra óptica, cable, túnel, etc. Las lineas, en el caso de los cables, de momento no dicen por dónde pasan.
* Estrellas: se visualiza de esta manera todo nodo/ubicación/punto que tenga más de un trasto/cacharro/dispositivo

### ¿El SN al que me conecto debe estar apuntando hacia mi antena?

Cuanto mayor sea la alinación entre los dos puntos mejor será la señal. Normalmente se instalan antenas omnidireccionales para dar una señal de 360º

### ¿Cómo averiguo si el nodo que está cerca de mí encara hacia mi antena y puede darme una buena señal?

Se puede hacer por aproximaciones. Si te guías por alguien que ya forma parte de guifi o tiene experiencia, la aproximación será mejor. Especialmente, compartir esta información con quien vas a conectar puede ayudar mucho.

1. La más sencilla: hay visibilidad directa entre los nodos.
2. Comprobar que las elevaciones son apropiadas para las zonas fresnel con esta aplicación. Alerta, no tiene en cuenta edificios, solo terreno. Lo cual lo hace más fiable en entorno rural http://wisp.heywhatsthat.com/
3. Hacer una prueba de cobertura: comprar una antena, o preguntar en tu comunidad si hay disponible una antena para hacer pruebas, o que un voluntario o instalador nos ayude. Cuanto más realista sea la prueba, mejor aproximación será. Necesitaremos un palo y conexión eléctrica allí donde haremos la prueba. Por ejemplo, durante esta prueba usar la conexión con el uso previsto a ver qué tal funciona. Y tratar de ponerla en la ubicación donde sería la instalación definitiva. Esta es la prueba más fiable, si funciona bien, la instalación final también.

### Qué frecuencia es mejor ¿2.4 GHz o 5 GHz?

Actualmente las ciudades estan saturadas de la frecuencia 2.4 GHz por lo que se recomienda usar 5 GHz

### ¿Puedo conectar mi antena de 5 Ghz a un nodo de 2.4 Ghz o al revés?

No. Antes de comprar el equipo debes tener bien claro a que SN vas a conectarte y a que frecuencia trabaja. Hay antenas que son de doble banda (2.4 y 5 GHz) pero es improbable que la tuya lo sea.

### ¿Cómo averiguo el tipo de antena que tiene y a que frequencia trabaja el nodo al que quiero conectarme?

La aplicación de guifi.net es en sí una base de datos gelocalizada que da información sobre sus nodos y sus dispositivos, y sobre las personas que los gestionan. Adicionalmente, otras herramientas pueden ser el contacto con sus administradores vía correo electrónico, chat, listas de correo, foro, en persona, etc.

### ¿Que puede hacer un instalador por mí?

En pocas palabras: garantizar que la instalación va a salir bien. Esto es especialmente importante si el colectivo que gestiona el espacio quiere depositar la confianza de la instalación en alguien que presuntamente lo va a ejecutar de forma profesional y que va a aportar a través de su experiencia, certificados, responsabilidad, reputación, etc.
