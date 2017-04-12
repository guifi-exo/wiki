#!/usr/bin/python3

# author: guifipedro
# license: GPLv3+

import ipaddress

# used to exit program -> http://stackoverflow.com/questions/73663/terminating-a-python-script
import sys

from dns import resolver,reversename
from dns.exception import DNSException,Timeout

# parse argument
import argparse
from argparse import RawTextHelpFormatter

# multiline description -> http://stackoverflow.com/questions/3853722/python-argparse-how-to-insert-newline-in-the-help-text/3853776#3853776
parser = argparse.ArgumentParser(description = """
What is about? This tool checks if an IP or range of IPs have a good "resolution of reverse" and "resolution of reverse resolution".
An error means that the IP does not comply with RFC1912 in that part:
PTR records must point back to a valid A record [or AAAA record], not a alias defined by a CNAME.""", formatter_class=RawTextHelpFormatter)
parser.add_argument("argument", help="As argument supports: an IPv4, an IPv6, a network in CIDR notation IPv4, a network in CIDR notation IPv6.")
args = parser.parse_args()
argument = args.argument

detect_cidr = argument.find('/')

ipv_version=None

# network of 1 IP :)
if detect_cidr == -1:
    try:
        network = ipaddress.ip_address(argument)
        ip_version = network.version
        network = iter([str(network)])
    except ValueError:
        print("Error: Invalid argument.\nYou entered an invalid IP as argument of this program. Should be something like a.b.c.d in IPv4. In case of IPv6, check how to write it")
        sys.exit(1)

# network of n IPs
else:
    try:
        network = ipaddress.ip_network(argument, strict=False)
        ip_version = network.version
        network = iter(network)
    except ValueError:
        print("Error: Invalid argument.\nYou entered an invalid network as argument of this program. Should be something like a.b.c.d/e in IPv4. In case of IPv6, check how to write it")
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
        if ip_version == 4:
            ip_r_ip = str(resolver.query(r_ip,"A")[0])
        else: # IPv6
            ip_r_ip = str(resolver.query(r_ip,"AAAA")[0])
    except DNSException:
        print(" ERROR  | %s => %s => NULL" % (ip, r_ip))
    else:
        print("  OK    | %s => %s => %s" % (ip, r_ip, ip_r_ip))
