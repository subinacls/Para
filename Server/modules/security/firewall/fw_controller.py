#!/usr/bin/env python

from os import popen

class FirewallActions:
    def __init__(self):
        pass

    def send_commands(self, cmds):
        sc = popen(cmds).readlines()
        if sc:
            print("Send commands returned:\n%s" % sc)
        return 1

    def init_fw(self, srv_port):
        # Initial firewall configuration
        # Redirect all ports to a single threaded server listening on the given server port
        # This is usually kicked off by the server automatically
        ifwc = "iptables -t nat -F;"
        ifwc += "iptables -t nat -I PREROUTING -p tcp --dport 1:65534 -j REDIRECT --to-ports %s;" % srv_port
        ifwc += "iptables -t nat -I OUTPUT -p tcp -d 127.0.0.1 --dport 1:65534 -j REDIRECT --to-port %s;" % srv_port
        ifwc += "iptables -t nat -I PREROUTING -p tcp --dport 65535 -j REDIRECT --to-ports 22;"
        ifwc += "iptables -t nat -I OUTPUT -p tcp -d 127.0.0.1 --dport 65535 -j REDIRECT --to-port 22;"
        self.send_commands(ifwc)
        return 1

    def rejected_fw(self):
        ipsfw = 'ipset create rejected hash:net'
        self.send_commands(ipsfw)
        return 1

    def trusted_fw(self):
        ipsfw = 'ipset create trusted hash:net'
        self.send_commands(ipsfw)
        return 1

    def add_trusted(self, client_ip):
        try:
            if "/" in str(client_ip):
                ipsfw = 'ipset add trusted %s' % client_ip
            else:
                ipsfw = 'ipset add trusted %s/32' % client_ip
            self.send_commands(ipsfw)
        except Exception as add_trusted_failed:
            print("ipset add trusted failed:\n\t%s" % add_trusted_failed)
        return 1

    def add_rejected(self, client_ip):
        try:
            if "/" in str(client_ip):
                ipsfw = 'ipset add rejected %s' % client_ip
            else:
                ipsfw = 'ipset add rejected %s/32' % client_ip
            self.send_commands(ipsfw)
        except Exception as add_rejected_failed:
            print("ipset add rejected failed:\n\t%s" % add_rejected_failed)
        return 1

    def ipset_match(self):
        ipsfw = 'iptables -A INPUT -m set --match-set trusted src -p tcp -m multiport --dports 1:65535 -j ACCEPT;'
        ipsfw += 'iptables -A INPUT -m set --match-set rejected src -p tcp -m multiport --dports 1:65535 -j DROP;'
        self.send_commands(ipsfw)
        return 1

    def ipset_save(self):
        ipss = 'ipset save /root/ipset_saved'
        self.send_commands(ipss)
        return 1

    def ipset_load(self):
        ipsl = 'ipset load /root/ipset_saved'
        self.send_commands(ipsl)
        return 1

    def iptables_save(self):
        ipts = 'iptables-save >/root/iptables-saved'
        self.send_commands(ipts)
        return 1

    def iptables_load(self):
        iptl = 'iptables-restore < /root/iptables-saved'
        self.send_commands(iptl)
        return 1

    def f2b_rework(self):
        try:
            input_work = 0
            for xa in popen('iptables -L INPUT --line-numbers').readlines():
                if xa.find('f2b-sshd') >= 0 and xa.find('anywhere') >= 0:
                    input_work = 1
            if input_work >= 1:
                ipfw = 'iptables -D INPUT %d ' % int(xa.split()[0])
                self.send_commands(ipfw)
                input_work = 0

            chain_work = 0
            for xa in popen('iptables -L f2b-sshd --line-numbers').readlines():
                if xa.find('RETURN') >= 0 and xa.find('anywhere') >= 0:
                    chain_work = 1
            if chain_work >= 1:
                ipfw = 'iptables -D "f2b-sshd" %d ' % int(xa.split()[0])
                self.send_commands(ipfw)
                ipfw = 'iptables -X "f2b-sshd" '
                self.send_commands(ipfw)
                chain_work = 0

            if input_work == 0:
                ipfw = 'iptables -N f2b-sshd'
                self.send_commands(ipfw)
                ipfw = 'iptables -A f2b-sshd -j RETURN '
                self.send_commands(ipfw)

            if chain_work == 0:
                ipfw = 'iptables -I INPUT -p tcp --match multiport --dports 1:65535 -j f2b-sshd '
                self.send_commands(ipfw)

        except Exception as f2b_rework_fail:
            print("F2b failed to reconfigure iptables:\n\t%s" % f2b_rework_fail)
        return 1

fw_actions = FirewallActions()
fw_actions.f2b_rework()
