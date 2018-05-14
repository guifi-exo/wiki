# Using a raspberry pi to unbrick a router
During Battlemesh I learned how to unbrick a TP-Link router using a Raspberry Pi.
## Prerequisites
- Raspberry Pi.
- An EEPROM programmer clip (~2 euros from Aliexpress). 
- Some jumper cable.
- The specific datasheet of your EEPROM.
- Common sense.
- A non-bricked router from which you can make a dump (or a dump, that some of your friends have created).
# Setup your Pi
To enable the SPI GPIO add this to /boot/config.txt:
```
dtparam=spi=on
```

Now run `raspi-config` and enable loading of the spi drivers (its under interfacing options --> spi) at boot. ([source](https://www.raspberrypi.org/documentation/hardware/raspberrypi/spi/README.md))

If you don't want to do this you can manually load your spi drivers using:
```
modprobe spi_bcm2835 # If that fails you may want to try the older spi_bcm2708 module instead
modprobe spidev
```
([source](https://www.flashrom.org/RaspberryPi))
## Setting up your cable
Find a datasheet of your flashchip and connect the right [GPIO](https://www.raspberrypi.org/documentation/usage/gpio/) pins to your programmer clip. 

Apply your clip carefully on the chip. My SSH session to the Raspberry Pi broke when I was doing this, probably because your Pi is powering part of your router, so make sure your USB adapter is adequate. 

## Reading
With your router powered off:
```
flashrom -p linux_spi:dev=/dev/spidev0.0,spispeed=1000 -r out2.img
```
Create 3 dumps & verify with `md5sum` to make sure all images are the same, if not you should try switching your router on.

## Writing
The same applies to writing:
```
flashrom -p linux_spi:dev=/dev/spidev0.0,spispeed=1000 -w out2.img -V
```

