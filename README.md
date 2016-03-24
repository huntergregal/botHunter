# botHunter
Scans the internet for open FTP servers looking for common malware bot droppers and grabs them for sampling. Also provides support for uploading samples to VirusTotal.

##Requirements
------------

The **netaddr** module must be installed, on Debian/Ubuntu systems simply run:

```
sudo apt-get install python3-pip
sudo pip3 install netaddr
```

Using Python 3 is recommended, but it should run on 2.x just fine.

##Install
-------

Clone this repository or save <a href="https://github.com/huntergregal/botHunter/botHunter.py">botHunter.py</a> on your machine and make it executable:

```
wget https://github.com/huntergregal/botHunter/botHunter.py
chmod +x ./botHunter.py
```

##Usage
-----

```
usage: botHunter.py [-h] [-t MAXTHREADS] [-w TIMEOUT] [-s]
                     [targets [targets ...]]

positional arguments:
  targets

optional arguments:
  -h, --help            show this help message and exit
  -t MAXTHREADS, --threads MAXTHREADS
                        Number of threads to use, default is 10
  -w TIMEOUT, --wait TIMEOUT
                        Seconds to wait before timeout, default is 2
  -s, --shuffle         Shuffle the target list
```

##Examples
--------

The syntax for specifying targets is similar to nmap. Here are some examples:

Scan three individual IPs:
```
./botHunter.py 192.168.1.1 192.168.1.2 192.168.1.3
```

Scan an entire IP-block using <a href="http://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing#CIDR_notation">CIDR notation</a> (in this example, all hosts from 192.168.1.1 - 192.168.1.254 will be scanned, a total of 254 hosts):
```
./botHunter.py 192.168.1.0/24
```

Feed targets from a other programm using a pipe (must be IPs, seperated by newlines!): 
```
cat mytargets.txt | ./botHunter.py
'''
'''
Scanning based on https://github.com/kennell/ftpknocker -- Copyright (c) 2014, kevin@fileperms.org All rights reserved.
'''


