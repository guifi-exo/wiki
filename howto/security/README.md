# browsers vulnerabilities

- https://thejh.net/misc/website-terminal-copy-paste

- https://arstechnica.com/security/2017/04/chrome-firefox-and-opera-users-beware-this-isnt-the-apple-com-you-want/
    - chrome/chromium: patched!
    - firefox: they won't fix. but in about config you can put "network.IDN_show_punycode" to true

# curl vulnerabilities
 
https://jordaneldredge.com/blog/one-way-curl-pipe-sh-install-scripts-can-be-dangerous/

# entropy

The plain simple reality of entropy Or how I learned to stop worrying and love urandom https://media.ccc.de/v/32c3-7441-the_plain_simple_reality_of_entropy#video&t=6

csprng

reusing the same key for different packets / messages

if we can trust urandom, this is a good password generator

```
ncharacters=12
npasswords=15
< /dev/urandom tr -dc 'a-zA-Z0-9-_' | fold -w $ncharacters | head -n $npasswords
```

# More resources

https://www.criptica.org/wiki
