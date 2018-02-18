# common start

download required packages: https://github.com/libremesh/lime-sdk#building-in-running-system

you require some space. ubnt-nano-m-xw takes ~900 MB

go inside repo

    git clone https://github.com/libremesh/lime-sdk
    cd lime-sdk

download feeds

    ./cooker -f

apply patches

    snippets/regdbtz.sh
    snippets/regdbus.sh

## option1: if you don't have kernel patches to apply

build archictecture

    ./cooker -b=ar71xx/generic

build specific device, for example:

    ./cooker -c ar71xx/generic --profile=ubnt-nano-m-xw --flavor=lime_default --remote --community=qmp/v1

## option2: if you have kernel patches to apply

apply patch, for example:

    snippets/regdbtz.sh

ibuild architecture and force all compilations locally or it will not apply

    ./cooker -b=ar71xx/generic --force-local

build specific device, for example:

    ./cooker -c ar71xx/generic --profile=ubnt-nano-m-xw --flavor=lime_default --community=qmp/v1

# qMp compatibility - known problems

- DHCP can be down for 5 min. Probably the workaround is to use odhcp instead of dnsmasq https://github.com/libremesh/network-profiles/blob/master/kollserola/generic/etc/uci-defaults/zz-use-odhcpd
    - https://github.com/libremesh/lime-web/issues/55
- essential is has name advanced in menu tab? http://10.202.45.1/cgi-bin/luci/lime/essentials
- Wifi settings in http://10.202.45.1/cgi-bin/luci/lime/essentials.
    - Select wifi channel requires typing. We need a combobox
    - No field to change 20 Mhz or 40 Mhz. Combobox?

# Q&A

- Q: I don't know what are the available architectures
    - A: target list (choose device's architecture)
        ./cooker --targets

- Q: My wifi is not working, how can I debug wifi?
    - A: `iwinfo`, `iw list`, `iw dev`

# extra

the new steps in qmp at the bottom: http://qmp.cat/News/35_qMp_4.0_Macondo_released
