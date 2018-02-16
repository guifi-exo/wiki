# build a libremesh that is compatible with qMp

**warning: not tested**

download required packages: https://github.com/libremesh/lime-sdk#building-in-running-system

go inside repo

    git clone https://github.com/libremesh/lime-sdk
    cd lime-sdk

target list

    ./cooker --targets

profile list

    ./cooker --profiles=ar71xx/generic

commonly

    snippets/regdbtz.sh
    ./cooker -c ar71xx/generic --profile=ubnt-nano-m-xw --flavor=lime_default --remote --community=qMp/v1
