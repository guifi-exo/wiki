# install

requirements:

    apt install gnupg2

# generate key

interactive

    gpg2 --gen-key

autogenerate key **without password**

```bash
gpg2 --batch --generate-key <<EOF
%echo Generating a basic OpenPGP key
Key-Type: RSA
Key-Length: 2048
Name-Real: username
Name-Comment: a useful comment
Name-Email: user@example.com
Expire-Date: 0
%no-protection
# Do a commit here, so that we can later print "done" :-)
%commit
%echo done
EOF
```

autogenerate key **with password**

```bash
gpg2 --batch --generate-key <<EOF
%echo Generating a basic OpenPGP key
Key-Type: RSA
Key-Length: 2048
Name-Real: username
Name-Comment: a useful comment
Name-Email: user@example.com
Expire-Date: 0
Passphrase: thisismypassphrase
# Do a commit here, so that we can later print "done" :-)
%commit
%echo done
EOF
```

# remove key

note: the key id that you can use is flexible, except if you want to destroy it in one step with `--batch --yes`

use `gpg2 --list-keys` or `gpg2 --list-secret-keys`

after you know the fingerprint you can remove it directly in one step

    gpg2 --batch --yes --delete-secret-and-public-key XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

alternatively

in two steps (4 confirmations)

    gpg2 --delete-secret-key user-identifier
    gpg2 --delete-key user-identifier

in one step (4 confirmations)

    gpg2 --delete-secret-and-public-key user-identifier

# import key

write command

    gpg2 --import

after enter, paste:

    -----BEGIN PGP PUBLIC KEY BLOCK-----
    
    (...)
    -----END PGP PUBLIC KEY BLOCK-----

then press enter and after that Ctrl+d

# export key

the key id that you can use is flexible

    gpg2 --armor --export <user-identifier>

# encrypt message

## public-private key

you send the message to a specific public key (a specific person)

way1: write in console

    gpg2 --encrypt --sign --armor -r <user-identifier>

paste secret

then press enter and after that Ctrl+d

way2: do it to a file

    gpg2 --encrypt --sign -r <user-identifier>

paste secret

then press enter and after that Ctrl+d

## symmetric

you just need to know the password

way1: write in console

    gpg2 --symmetric --sign --armor

paste secret

then press enter and after that Ctrl+d

way2: do it to a file

    gpg2 --symmetric --sign

paste secret

then press enter and after that Ctrl+d

# decrypt message

   gpg2 

then paste message

then press enter and after that Ctrl+d

# trust key

    gpg2 --edit-key <user-identifier>

then type

    trust

decide

# lists

print fingerprints

    gpg2 --fingerprints

print public keys

    gpg2 --list-public-keys

print private keys

    gpg2 --list-secret-keys

# extra references

https://github.com/dashohoxha/egpg

https://wiki.archlinux.org/index.php/GnuPG
