#!/usr/bin/env python
#
# Encrypt data with known key (Server Side)
#

from os import popen as po
from yaml import load as yl

class Encryption:
    def __init__(self):
        pass

    @staticmethod
    def encrypt_with_key(password, datastream):
        try:
            rdata = po('echo ' + str(datastream) +
                       ' | openssl enc -aes-256-cbc -base64 -pass pass:' + str(password) +
                       ' 2>/dev/null | tr -d " \n"').readlines()[0].strip()
            return rdata
        except Exception as decode_fail:
            return 0
