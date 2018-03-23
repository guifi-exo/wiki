# gluster

## manteniment

al apagar i tornar a encendre un node del gluster s'ha de comprovar fins que surt tot 0 i després espera 10 min i que torni a sortir tot zero

    gluster volume heal vmstore info | grep -i entries
