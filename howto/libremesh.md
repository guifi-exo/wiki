# build a libremesh that is compatible with qMp

**warning: not tested**

download required packages: https://github.com/libremesh/lime-sdk#building-in-running-system

go inside repo

    git clone https://github.com/libremesh/lime-sdk
    cd lime-sdk

apply patch

    ./cooker -f
    snippets/regdbtz.sh

target list (choose device's architecture)

    ./cooker --targets

profile list (choose device)

    ./cooker --profiles=ar71xx/generic

commonly

    ./cooker -c ar71xx/generic --profile=ubnt-nano-m-xw --flavor=lime_default --remote --community=qmp/v1

note: cooking required ~900 MB
