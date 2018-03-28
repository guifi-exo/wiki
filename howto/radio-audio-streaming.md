## icecast

we assume that SSL/TLS/HTTPS is important, that's why we are compiling it. if you don't care about this just `apt install icecast2` is fine

why we need to compile to get "security" capabilities:

- https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=744815
- https://trac.xiph.org/ticket/2310

```
apt-get build-dep icecast2
# trust me: https://downloads.xiph.org/releases -> https://ftp.osuosl.org/pub/xiph/releases/
wget https://ftp.osuosl.org/pub/xiph/releases/icecast/icecast-2.4.3.tar.gz
tar xvf icecast-2.4.3.tar.gz
cd icecast-2.4.3
./configure
make
make install
```

install icecast2 to get the service

    apt install icecast2

change /etc/init.d/icecast2

    #DAEMON=/usr/bin/icecast2
    DAEMON=/usr/local/bin/icecast

replace:

```
    <paths>
        <!-- basedir is only used if chroot is enabled -->
        <basedir>/usr/share/icecast2</basedir>

        <!-- Note that if <chroot> is turned on below, these paths must both
             be relative to the new root, not the original root -->
        <logdir>/var/log/icecast2</logdir>
        <webroot>/usr/share/icecast2/web</webroot>
        <adminroot>/usr/share/icecast2/admin</adminroot>
```

with:

```
    <paths>
        <!-- basedir is only used if chroot is enabled -->
        <basedir>/usr/local/share/icecast</basedir>

        <!-- Note that if <chroot> is turned on below, these paths must both
             be relative to the new root, not the original root -->
        <logdir>/var/log/icecast2</logdir>
        <webroot>/usr/local/share/icecast/web</webroot>
        <adminroot>/usr/local/share/icecast/admin</adminroot>
```

then we can remove icecast2 debian package

    apt remove icecast2

assuming you configured successfully a certbot / letsencrypt HTTPS certificate:

    cat /etc/letsencrypt/live/example.com/cert.pem /etc/letsencrypt/live/example.com/privkey.pem > /usr/local/share/icecast/icecast.pem

TODO cron, seems that I need to restart icecast (!) and this breaks the streaming :(

TODO exchange between certbot and snakeoil cert using "reload"

references:

- check ssl in compilation src https://jksinton.com/articles/rpi-compiling-icecast-support-openssl
- service stuff inspired by src https://stackoverflow.com/questions/42188137/how-to-make-icecast-as-service-and-restart-it

## libretime

don't do this on a public server !!

```
git clone https://github.com/LibreTime/libretime
cd libretime
./install -p -i -a
```

### docs

switching between live and scheduled playout https://www.youtube.com/watch?v=qRqYtNsg-UM

## liquidsoap

## install

convince yourself early that you need to compile yourself liquidsoap (if you are on debian 9 stretch on 2018-03-26) - https://github.com/LibreTime/libretime/issues/192

is required to send signals and to have libretime working

to install icecast2 is enough to `apt install icecast2` and put appropriate passwords to avoid intrusion

### method 1 - latest version

only first and last command as root, later we use a specific user

```
apt install opam

adduser liquidsoap
gpasswd -a liquidsoap sudo

su -l liquidsoap 

opam init -a # and say yes

opam config env

# general
# next command will need sudo
opam depext taglib mad lame vorbis cry samplerate liquidsoap opus
opam install taglib mad lame vorbis cry samplerate liquidsoap opus

# if is for your laptop and you want to use microphone input
opam depext pulseaudio
opam install pulseaudio
```

install "using opam" -> src http://liquidsoap.info/download.html

#### daemonize

```
# if is going to be a service running permanently
opam install liquidsoap-daemon
daemonize-liquidsoap.sh
```

modify accordingly `~/script/main.liq`

after that:

    systemctl status main-liquidsoap.service 

### method 2 - DYI

```
apt-get build-dep liquidsoap
apt-get source liquidsoap
cd liquidsoap-<version>
./configure
make
make install
```

src http://wiki.occupyboston.org/wiki/Multi-usb_mic/jackd/liquidsoap_setup

### sending signals

send mp3 file (that loops indefinetely) or your input microphone (using pulseaudio)

explanation for jack -> src http://wiki.occupyboston.org/wiki/Multi-usb_mic/jackd/liquidsoap_setup

send directly to icecast 

```liquidsoap
#!/usr/bin/liquidsoap
set("log.file.path", "/path/to/liq.log")
signal = single("/path/to/song.mp3")
#signal = input.pulseaudio(clock_safe=false)
output.icecast(%mp3,
     host = "<ip or URL>", port = 8000,
     password = "hackme", mount = "jazz.mp3",
     mksafe(signal))
```

send to libretime to master source

```liquidsoap
#!/usr/bin/liquidsoap
set("log.file.path", "/path/to/liq.log")
signal = single("/path/to/song.mp3")
#signal = input.pulseaudio(clock_safe=false)
output.icecast(%mp3,
     host = "<ip or URL>", port = 8001,
     password = "hackme", mount = "master",
     mksafe(signal))
```
