#!/usr/bin/env python
#
# Decrypt data with known key (Server Side)
#

from os import popen
from yaml import load

class Decryption:
    def __init__(self):
        pass

    @staticmethod
    def known_host_decrypt(host_list, data_stream):
        try:
            for host in host_list:
                rdata = popen('echo ' + str(data_stream) +
                              '| base64 -d | openssl enc -aes-256-cbc -d -pass pass:' + str(host) +
                              ' 2>/dev/null').readlines()[0].strip()
            if load(rdata):
                return host, rdata
        except Exception as known_host_wkey_failed:
            return 0

    @staticmethod
    def decrypt_with_key(password, data_stream):
        try:
            rdata = popen('echo ' + str(data_stream) +
                          '| base64 -d | openssl enc -aes-256-cbc -d -pass pass:' + str(password) +
                          ' 2>/dev/null').readlines()[0].strip()
            return rdata
        except Exception as decrypt_with_key_failed:
            return 0
