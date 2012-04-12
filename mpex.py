#!/usr/bin/python

import gnupg
import urllib
import urllib2
import sys

class MPEx:
    def __init__(self, passphrase):
        self.gpg = gnupg.GPG()
        self.passphrase = passphrase
        self.mpex_url = 'http://polimedia.us/bitcoin/mpex.php'

    def command(self, command):
        signed_data = self.gpg.sign(command, passphrase=self.passphrase)
        encrypted_ascii_data = self.gpg.encrypt(str(signed_data), ['F1B69921'], passphrase=self.passphrase, always_trust=True)
        data = urllib.urlencode({'msg' : str(encrypted_ascii_data)})
        req = urllib2.Request(self.mpex_url, data)
        response = urllib2.urlopen(req)
        result = response.read()
        return self.gpg.decrypt(result, passphrase=self.passphrase, always_trust=True)

if __name__ == '__main__':
    from getpass import getpass
    passphrase = getpass("Enter your GPG passphrase: ")
    mpex = MPEx(passphrase)
    print mpex.command(sys.argv[1])
