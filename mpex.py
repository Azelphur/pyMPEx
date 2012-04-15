#!/usr/bin/python

import gnupg
import urllib
import urllib2
import sys

class MPEx:
    def __init__(self):
        self.gpg = gnupg.GPG()
        self.mpex_url = 'http://polimedia.us/bitcoin/mpex.php'
        self.mpex_fingerprint = 'F1B69921'
        self.passphrase = None

    def command(self, command):
        if self.passphrase == None: return None
        signed_data = self.gpg.sign(command, passphrase=self.passphrase)
        encrypted_ascii_data = self.gpg.encrypt(str(signed_data), self.mpex_fingerprint, passphrase=self.passphrase)
        data = urllib.urlencode({'msg' : str(encrypted_ascii_data)})
        req = urllib2.Request(self.mpex_url, data)
        response = urllib2.urlopen(req)
        result = response.read()
        reply = str(self.gpg.decrypt(result, passphrase=self.passphrase))
        if reply == '': return None
        return reply

    def checkKey(self):
        keys = self.gpg.list_keys()
        for key in keys:
            if key['fingerprint'] == self.mpex_fingerprint:
                return True
        return False

if __name__ == '__main__':
    from getpass import getpass
    mpex = MPEx()
    if not mpex.checkKey():
        print 'You have not added MPExes keys. Please run...'
        print 'gpg --search-keys "F1B69921"'
        print 'gpg --sign-key F1B69921'
        exit()
    if len(sys.argv) != 2:
        print 'Usage: mpex.py <command>'
        print 'Example: mpex.py STAT'
        exit()
    mpex.passphrase = getpass("Enter your GPG passphrase: ")
    reply = mpex.command(sys.argv[1])
    if reply == None:
        print 'Couldn\'t decode the reply from MPEx, perhaps you didn\'t sign the key? try running'
        print 'gpg --sign-key F1B69921'
        exit()
    print reply

