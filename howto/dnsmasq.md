# As DNS / caching DNS

Recommended starting config for `/etc/dnsmasq.conf`

```
# caching -> src https://www.g-loaded.eu/2010/09/18/caching-nameserver-using-dnsmasq/
cache-size=1000

# more than three nameservers -> src https://wiki.archlinux.org/index.php/dnsmasq#More_than_three_nameservers
#resolv-file=/etc/resolv.dnsmasq.conf

# src http://bradmont.net/posts/dnasmasq_multiple_ips/
localise-queries

# don't include /etc/hosts
no-hosts
# cancel specific cnames in alternative file than /etc/hosts
#addn-hosts=/etc/hosts.dnsmasq.conf

# massive blocking a specific domain this -> src https://stackoverflow.com/questions/22313142/wildcard-subdomains-with-dnsmasq
address=/specific.subdomain.exo.cat/0.0.0.0

# log stuff -> src https://bbs.archlinux.org/viewtopic.php?id=78547
log-queries
log-facility=/var/log/dnsmasq.log
```
