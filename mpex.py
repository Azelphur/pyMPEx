#!/usr/bin/python

import gnupg
import urllib
import urllib2
import sys
from decimal import Decimal
SATOSHI = Decimal('100000000.0')

class MPEx:
    def __init__(self):
        self.gpg = gnupg.GPG()
        self.mpex_url = 'http://mpex.co'
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
        if not self.gpg.verify(reply):
            print '!!!WARNING!!!'
            print 'Invalid Signature, do not trust this data.'
        if reply == '': return None
        return reply

    def checkKey(self):
        keys = self.gpg.list_keys()
        for key in keys:
            if key['fingerprint'].endswith(self.mpex_fingerprint):
                return True
        return False

    def confirm(self,command):
        msg = "Execute '"+ command+"'"
        cmd = command.split('|')
        if cmd[0] in ('BUY','SELL'):
            msg = msg + ", total " + str(Decimal(cmd[2])*Decimal(cmd[3])/SATOSHI) + "BTC"
        elif cmd[0] == 'WITHDRAW':
            msg = msg + ", " + str(Decimal(cmd[2])/SATOSHI) +"BTC"
        msg += " (y/n)?"
        res = raw_input(msg)
        return res == 'y'

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
    if not mpex.confirm(sys.argv[1]):
        exit()
    mpex.passphrase = getpass("Enter your GPG passphrase: ")
    reply = mpex.command(sys.argv[1])
    if reply == None:
        print 'Couldn\'t decode the reply from MPEx, perhaps you didn\'t sign the key? try running'
        print 'gpg --sign-key F1B69921'
        exit()
    print reply

