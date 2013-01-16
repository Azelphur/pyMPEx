#!/usr/bin/python

import gnupg
import urllib
import urllib2
import sys
from decimal import Decimal
from argparse import ArgumentParser
from datetime import datetime
SATOSHI = Decimal('100000000.0')

def parse_args():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("command", help="MPEx command. It is necessary to quote it because of '|' special character, like: \"BUY|S.MPOE|1|100000\" ")
    parser.add_argument("-y","--noconfirm", help="disable confirmation prompt", action='store_true', required = False)
    parser.add_argument("-a","--use_agent", help="use GPG agent instead of asking for passphrase", action='store_true', required = False)
    parser.add_argument("-l","--logfile", help="append command, encrypted and decrypted output to this logfile. By default mpex.log in current directory is used. Use -l - to disable file logging completely.", required = False)
    args = parser.parse_args()
    return args

class MPEx:
    def __init__(self, use_agent = False, logfile=True):
        self.gpg = gnupg.GPG(use_agent=use_agent)
        self.mpex_url = 'http://mpex.co'
        self.mpex_fingerprint = 'F1B69921'
        self.passphrase = None
        self.log = None
        if(logfile):
            if(logfile == True):
                logfile = "mpex.log"
            self.log = open(logfile,'a')

    def command(self, command):
        if (self.log) :self.log.write(datetime.now().isoformat() + " " +command + "\n")
        signed_data = self.gpg.sign(command, passphrase=self.passphrase)
        encrypted_ascii_data = self.gpg.encrypt(str(signed_data), self.mpex_fingerprint, passphrase=self.passphrase)
        data = urllib.urlencode({'msg' : str(encrypted_ascii_data)})
        req = urllib2.Request(self.mpex_url, data)
        response = urllib2.urlopen(req)
        result = response.read()
        if (self.log) :self.log.write(datetime.now().isoformat() + " " +result+ "\n")
        reply = str(self.gpg.decrypt(result, passphrase=self.passphrase))
        if not self.gpg.verify(reply):
            print '!!!WARNING!!!'
            print 'Invalid Signature, do not trust this data.'
        if reply == '': return None
        if (self.log) : self.log.write(datetime.now().isoformat() + " " +reply+"\n")
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
        elif cmd[0] in ('STAT','STATJSON'):
            #mostly harmless
            return True
        msg += " (y/n)?"
        res = raw_input(msg)
        return res == 'y'

if __name__ == '__main__':
    from getpass import getpass
    args = parse_args()
    if args.logfile in ('-' ,''):
        logfile = False  
    elif args.logfile == None:
        #not specified - use default log file
        logfile = True
    else:
        logfile = args.logfile
    mpex = MPEx(args.use_agent, logfile)
    if not mpex.checkKey():
        print 'You have not added MPExes keys. Please run...'
        print 'gpg --search-keys "F1B69921"'
        print 'gpg --sign-key F1B69921'
        exit()
    if not (args.noconfirm or mpex.confirm(args.command)):
        exit()
    if not args.use_agent:
        mpex.passphrase = getpass("Enter your GPG passphrase: ")
    reply = mpex.command(args.command)
    if reply == None:
        print 'Couldn\'t decode the reply from MPEx, perhaps you didn\'t sign the key? try running'
        print 'gpg --sign-key F1B69921'
        exit()
    print reply

