<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [icecast](#icecast)
- [libretime](#libretime)
  - [docs](#docs)
- [liquidsoap](#liquidsoap)
  - [install](#install)
    - [method 1 - latest version](#method-1---latest-version)
    - [method 2 - DYI](#method-2---dyi)
  - [daemonize](#daemonize)
  - [sending signals](#sending-signals)
  - [testing switch with (catalan) voice and sounds](#testing-switch-with-catalan-voice-and-sounds)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## icecast

we assume that SSL/TLS/HTTPS is important (we are going to achieve: https://example.com:8443), that's why we are compiling it. if you don't care about doing `apt install icecast2` is fine

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

uncomment this:

    <listen-socket>
        <port>8443</port>
        <ssl>1</ssl>
    </listen-socket>

uncomment / adapt:

    <ssl-certificate>/usr/local/share/icecast/icecast.pem</ssl-certificate>

We cannot change or renew certificate reloading the service -> src https://wiki.xiph.org/Icecast_Server/known_https_restrictions

TODO smart cron to minimize number of restarts of the service. (!) A restart is going to break the streaming

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

### install

convince yourself early that you need to compile yourself liquidsoap (if you are on debian 9 stretch on 2018-03-26) - https://github.com/LibreTime/libretime/issues/192

is required to send signals and to have libretime working

to install icecast2 is enough to `apt install icecast2` and put appropriate passwords to avoid intrusion

#### method 1 - latest version

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

#### method 2 - DYI

```
apt-get build-dep liquidsoap
apt-get source liquidsoap
cd liquidsoap-<version>
./configure
make
make install
```

src http://wiki.occupyboston.org/wiki/Multi-usb_mic/jackd/liquidsoap_setup

### daemonize

transform your liquidsoap script as a service

```
opam install liquidsoap-daemon
cd /to/the/directory/you/want/files/created # in my case: liked `cd ~`
daemonize-liquidsoap.sh
```

modify accordingly `~/script/main.liq`

after that:

    systemctl status main-liquidsoap.service 

src https://github.com/savonet/liquidsoap-daemon

next service would be

    daemonize-liquidsoap.sh newservice

and modify accordingly `~/script/newservice.liq`

to remove:

    mode=remove init_type=systemd daemonize-liquidsoap newservice

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

### testing switch with (catalan) voice and sounds

extra requirements (voice synthesis)

    apt install festival festvox-ca-ona-hts

add to `/etc/festival.scm`:

    (set! voice_default voice_upc_ca_ona_hts)

strings with accents will be destroyed, for example "interrupció" -> http://festcat.talp.cat/en/usage.php

```
# concat strings -> https://bytesandbones.wordpress.com/2014/07/18/liquidsoap-concat-strings/
# random weigths -> src "A simple radio" http://savonet.sourceforge.net/doc-svn/quick_start.html
def template(text, freq)
  msg = random(
    weights = [1, 2, 10],
    [
      single("say: #{text}"),
      sine(480.0, amplitude = 0.1, duration = 0.5),
      blank(duration = 1.0)
    ])
  add([sine(freq, amplitude = 0.05), msg], normalize = true)
end

# A simple cross-fade -> src "Switch-based transitions" http://savonet.sourceforge.net/doc-svn/cookbook.html
def crossfade(a,b)
  add(normalize=false,
      [ sequence([ blank(duration=1.),
                   fade.initial(duration=2.,b) ]),
        fade.final(duration=1.,a) ])
end

init = template("tros de 0 a deu segons cada minut", 800.0)
init2 = template("tros de trenta a quaranta cinc segons cada minut", 1500.0)
#p1 = template("program number 1")
p2 = template("programa de deu a catorze hores", 440.0)
p3 = template("programa de quinze a vint hores", 440.0)
default_source = template("programa per defecte", 440.0)

default_transition = [
  crossfade, # init
  crossfade, # init2
  crossfade, # p2
  crossfade, # p3
  crossfade # default source
]

signal = switch(
  track_sensitive = false,
  transitions = default_transition,
  [
    ({ 0s-10s }, init),
    ({ 30s-45s }, init2),
    ({ 10h-14h }, p2),
    ({ 15h-20h }, p3),
    ({ true }, default_source)
  ])

#out(signal)

output.icecast(%mp3,                                            
     host = "localhost", port = 8000,
     password = "hackme", mount = "test2.mp3",
     mksafe(signal))
```

### alternative to libretime/airtime

- main: take care of having always a fallback source (never stops, at the end we have silence running, and should never be modified or restarted). In this priority:
    - live1: intented to be for live with static icecast mountpoint
    - live2: intended to be for live with dynamic/spontaneous/ephemeral icecast mountpoint
    - schedule: executes the scheduled radio

```
su - liquidsoap
cd ~
daemonize-liquidsoap.sh main
daemonize-liquidsoap.sh live1
daemonize-liquidsoap.sh live2
daemonize-liquidsoap.sh schedule

# live1 and live2 should only be started manually
systemctl disable live1-liquidsoap.service 
systemctl disable live2-liquidsoap.service
```

files of the service -> https://github.com/guifi-exo/xrcb-scheduler

# other radios / examples

http://dir.xiph.org/
