# Quick install instructions

https://github.com/jitsi/jitsi-meet/blob/master/doc/quick-install.md

# Disable third party stuff

/etc/jitsi/meet/meet.tips.es-config.js

    disableThirdPartyRequests: true,

# Enable Screen Capture for Chromium/Chrome

## DIY

Do what official documentation says: https://github.com/jitsi/jidesha/blob/master/chrome/README.md#create-the-extension

I suggest:

    sudo apt install git
    git clone https://github.com/jitsi/jidesha
    cd jidesha

What is missing after that is how to generate the crx. Let's go!

Requirements for debian 9 (src https://stackoverflow.com/a/33432126):

    sudo apt install rubygems-integration ruby ruby-dev

After that install the application that does the crx

    sudo gem install crxmake

Assuming we are in the same directory (the git repository) we generate the pack extension with the chrome directory:

    crxmake --pack-extension chrome

after that you will see in the same directory `chrome.crx`

drag it to your extensions in chrome/chromium and copy the `id`

In your jitsi server (replace example.com with your domain) `/etc/jitsi/meet/meet.example.com-config.js` paste your `id`:

```diff
    - desktopSharingChromeExtId: 'diibjkoicjeejcmhdnailmkgecihlobk',
    + desktopSharingChromeExtId: 'myidisherelalalalalalalalalalala',
```

## Optional additional step: going official

If you want facilitate plugin installation (as you may see in meet.jit.si) you have to do the following:

- get developer account https://chrome.google.com/webstore/developer/dashboard
- pay 5$ (one time payment) - but you can register limited (20) number of applications in store -> src https://chrome.google.com/webstore/developer/about_signup
- Verify that this is an official item for a website you own (add new, select), scp html that gives google to /usr/share/jitsi-meet (remember to use https, and set https as the url, redirection won't work)
- check `inline install` -> src info about inline install https://developer.chrome.com/webstore/inline_installation?hl=en-US
- put `visibility options` as `unlisted`

# Enable Screen Capture for Firefox

```diff
    - desktopSharingFirefoxDisabled: true,
    + desktopSharingFirefoxDisabled: false,
    // (...)
    - desktopSharingFirefoxMaxVersionExtRequired: -1,
    + desktopSharingFirefoxMaxVersionExtRequired: 51,
```

src https://github.com/jitsi/jidesha/blob/master/firefox/README.md#deprecation

# Troubleshooting

Important logs to inspect

- /var/log/jitsi/jicofo.log - jitsi meet (javascript, and binding to videobridge and prosody)
- /var/log/jitsi/jvb.log - jitsi videobridge
- /var/log/prosody/prosody.log - XMPP server (chat, room allocation)

try restarting services (or reboot):

    service jicofo restart
    service jitsi-videobridge restart
    service prosody restart

# More info

- Jitsi Videobridge documentation - https://github.com/jitsi/jitsi-videobridge/blob/master/doc
