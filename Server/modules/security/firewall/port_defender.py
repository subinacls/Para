#!/usr/bin/env python

from os import popen
from threading import Thread
import time

class ScanMonitor:
    def __init__(self):
        self.cancelled = False

    def portscan_monitor(self):
        while not self.cancelled:
            self.monitor_conn()
            time.sleep(1)

    def monitor_conn(self):
        conns = {}
        for xa in popen('ss -ant | grep -Ev "State|LISTEN" | grep EST | tr -s " " | cut -d" " -f5').readlines():
            ip_addr = xa.split(":")[0].strip()
            port_num = xa.split(":")[1].strip()

            if ip_addr not in conns:
                conns[ip_addr] = []

            if port_num not in conns[ip_addr]:
                conns[ip_addr].append(port_num)

            if len(conns[ip_addr]) >= 5:
                ipset_ban = 'ipset add rejected %s 2>/dev/null' % ip_addr
                try:
                    popen(ipset_ban)
                except Exception as ipset_ban_failed:
                    pass
                conns[ip_addr] = []
                del conns[ip_addr]

        return conns

scan_monitor = ScanMonitor()
scan_monitor.portscan_monitor()

# Kill the process with the following call
# scan_monitor.cancelled = True
