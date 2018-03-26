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

convince yourself early that you need to compile yourself liquidsoap (if you are on debian 9 stretch on 2018-03-26)

is required to send signals and to have libretime working

to install icecast2 is enough to `apt install icecast2` and put appropriate passwords to avoid intrusion

### method 1 - latest version

```
apt install opam

opam init

opam config env

opam depext taglib mad lame vorbis cry samplerate liquidsoap opus pulseaudio

opam install taglib mad lame vorbis cry samplerate liquidsoap opus pulseaudio

ln -s /home/<user>/.opam/system/bin/liquidsoap /usr/bin/liquidsoap
```

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
