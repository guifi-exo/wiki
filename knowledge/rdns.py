#!/usr/bin/python3

# check if IPs of a network have good resolution of reverse and resolution of reverse
# author: guifipedro
# license: GPLv3+

# requirement: apt-get install python3-netaddr
import netaddr

# used to exit program -> http://stackoverflow.com/questions/73663/terminating-a-python-script
import sys

from dns import resolver,reversename
from dns.exception import DNSException,Timeout

# parse argument
import argparse

#sys.exit(0)

parser = argparse.ArgumentParser()
parser.add_argument("net", help="put ip you want to test")
args = parser.parse_args()
net = args.net

print("""
Note: Network identity and broadcast are not evaluated
Error means that the IP does not comply with RFC1912 in that part:
PTR records must point back to a valid A record, not a alias defined by a CNAME.
""")

try:
    # http://stackoverflow.com/questions/4525492/python-list-of-addressable-ip-addresses/4545864#4545864
    # list IPs
    network = list(netaddr.IPNetwork(net).iter_hosts())
except AddFormatError:
    print("Error1: You entered an invalid network as argument of this program. Should be something like a.b.c.d/e")
    sys.exit(1)

for ip in network:
    # dns lookups -> https://spareclockcycles.org/2010/04/13/reverse-dns-lookups-with-dnspython.html
    # in-addr.arpa. format
    ip = str(ip)
    addr = reversename.from_address(ip)
    try:
        r_ips = resolver.query(addr,"PTR")
    except Timeout:
        print("TIMEOUT | %s => NULL" % ip)
        continue
    except DNSException:
        print(" ERROR  | %s => NULL" % ip)
        continue
    
    r_ip = str(r_ips[0])

    if len(r_ips) > 1:
        print("multiple PTRs (took first):")
        # first example -> http://www.dnspython.org/examples.html
        for ptrs in r_ips:
            print ('Host', rdata.exchange, 'has preference', rdata.preference)

    ip_r_ip=None
    try:
        ip_r_ip = str(resolver.query(r_ip,"A")[0])
    except DNSException:
        print(" ERROR  | %s => %s => NULL" % (ip, r_ip))
    else:
        print("  OK    | %s => %s => %s" % (ip, r_ip, ip_r_ip))
