suggested tasks

- [ ] security by default https://gitlab.com/femprocomuns/ldapclient/issues/3 (abstract function of hash so it is used always). the problem is in `views.py` `def edit`, password is a plain text utf-8
- [ ] document how to put this application for production usage (flask application + apache?)
- [ ] migrate to python 3
- [ ] migrate from [pythonldap](https://github.com/python-ldap/python-ldap) library to [ldap3](https://github.com/cannatag/ldap3)

installation steps

```
git clone https://gitlab.com/femprocomuns/ldapclient

cd ldapclient

apt install python-pip python-virtualenv git

virtualenv --python=/usr/bin/python2.7 env

source env/bin/activate

pip install flask
apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev
pip install python-ldap

apt-get install libjpeg62-turbo libjpeg62-turbo-dev
pip install randomavatar

pip install flask_script flask_login flask_wtf
# and put appropriate config
cp config.cfg.example config.cfg

cd ..
cat > manage_ldap.py <<EOF
from flask_script import Manager, Server
from ldapclient import app

manager = Manager(app)

#Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    threaded = True,
    port = '5001',
    host = '0.0.0.0')
)

if __name__ == "__main__":
    manager.run()
EOF

chmod +x manage_ldap.py
manage_ldap.py runserver
```

another useful related application is https://gitlab.com/femprocomuns/onboarding when users actively want an account
