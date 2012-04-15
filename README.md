#About
This is a command line front end to MPEx. It is also a simple library for communication with MPEx.

#Install/Usage:
* [Get python-gnupg](http://code.google.com/p/python-gnupg/)
* Make sure you have signed MPEx's key using "gpg --sign-key F1B69921"
* Run ./mpex.py COMMAND
* You can find a list of valid commands on the [MPEx FAQ](http://polimedia.us/bitcoin/faq.html)

#Examples:
##From command line

>$ ./mpex.py STAT
Enter your GPG passphrase: 
-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA1

>Holdings for Alfie Day (fingerprint AF97CD440E9F6124753BADFF61AFBDB270AC7F3E)
Issued today, Sunday the 15th of April 2012 at 07:53:42 PM (0.85963600 1334519622)
To certify that the aforementioned holds as of the quoted time the following with MPEx :

>	CxBTC x 300.00000000

>To which add orders in the book fully paid in advance :


>To which add sums deposited as surety for underwritten option contracts :


>Your last few transactions :

>The Great Seal of the exchange has been duly applied.
-----BEGIN PGP SIGNATURE-----
Version: GnuPG v1.4.5 (GNU/Linux)

>iD8DBQFPiydGkhT8a/G2mSERAgeWAJ9HvByj+W3Ky1kBo6pvFgIFvVyZ8QCfVcHi
VbYO51QAGTV81rGdkcBxWtM=
=Vo1k
-----END PGP SIGNATURE-----

##As a library
```python
>>> from mpex import MPEx
>>> mpex = MPEx()
>>> mpex.passphrase = 'My_GPG_Passphrase'
>>> mpex.command('STAT')
'-----BEGIN PGP SIGNED MESSAGE-----\nHash: SHA1\n\nHoldings for...
```
