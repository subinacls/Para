#!/usr/bin/env python

from os import popen
from modules.system.syscalls import findapp as fa

class IPModify:
    def __init__(self):
        fa().findall()
        pass

    def ipset_list(self):
        trusted = popen('ipset list trusted 2>/dev/null').readlines()
        rejected = popen('ipset list rejected 2>/dev/null').readlines()
        if not trusted:
            popen('ipset create trusted hash:net').readlines()
        if not rejected:
            popen('ipset create rejected hash:net').readlines()
        return 1

    def add_trusted(self, client_ip):
        # Adds authenticated client to ipset list in CIDR form
        # If list does not exist, it will be generated on the first client entry
        if len(client_ip.split('/')) > 1:
            cmd = 'ipset add trusted %s' % client_ip
        else:
            cmd = 'ipset add trusted %s/32' % client_ip
        popen(cmd).readlines()
        return 1

    def add_rejected(self, client_ip):
        # Adds authenticated client to ipset list in CIDR form
        # If list does not exist, it will be generated on the first client entry
        if len(client_ip.split('/')) > 1:
            cmd = 'ipset add rejected %s' % client_ip
        else:
            cmd = 'ipset add rejected %s/32' % client_ip
        popen(cmd).readlines()
        return 1

    def allow_client(self, client_ip):
        # Append a client IP address to the trusted ipset list
        cmd = 'ipset add trusted %s' % client_ip
        popen(cmd).readlines()

    def iptable_manipulate(self):
        # Ensure ALL connections arrive before DROP/REJECTED list is processed
        popen('iptables -I INPUT -j ACCEPT').readlines()
        # Drop all rejected clients in iptables
        popen('iptables -I INPUT -m set --match-set rejected src -j DROP').readlines()
        # Permit trusted authenticated clients after DROP/REJECTED is processed
        popen('iptables -I INPUT -m set --match-set trusted src -j ACCEPT').readlines()
        return 1
