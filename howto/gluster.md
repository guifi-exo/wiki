# gluster

## manteniment

al apagar i tornar a encendre un node del gluster esperar 10 minuts al meys per assegurar-se que el self-heal ha fet la feina. Llavors comprovar que no hi han fitxers pendents amb:

    gluster volume heal vmstore info

amb més concreció, en:

    gluster volume heal vmstore info | grep -i entries

et surten tots a 0 cal esperar 10 minuts, tornar-ho a comprovar i si tot torna a sortir 0 llavors pots parar l'altre
