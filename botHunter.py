#!/usr/bin/env python
'''
Scanning code based on https://github.com/kennell/ftpknocker
'''


import ftplib
import sys, os
import threading
from argparse import ArgumentParser
from netaddr import IPSet
from random import shuffle

KNOWN_BOTS = ["pbot.php"]

#check for known bots
def bot_check(ftp, host):
	fileList = ftp.nlst()
	for knownBot in KNOWN_BOTS:
		for fileName in fileList:
			if fileName.lower() == knownBot.lower():
				outputFile = "output/%s-%s" % (host, fileName)
				print("[+] Potential bot found: %s  @@  %s") % (fileName, host)
				with open(outputFile, 'w') as f:
					try:
						ftp.retrbinary('RETR %s' % fileName, f.write)
					except Exception as e:
						print("Error getting file: %s" % repr(e))
#output dir
def check_output():
	if not os.path.exists("output"):
		os.makedirs("output")
# Split list
def split_list(l, parts):
	newlist = []
	splitsize = 1.0/parts*len(l)
	for i in range(parts):
		newlist.append(l[int(round(i*splitsize)):int(round((i+1)*splitsize))])
	return newlist

# Try anonymous FTP login
def try_ftp_login(hosts):
	for host in hosts:
		host = host.strip()
		try:
			ftp = ftplib.FTP()
			ftp.connect(host=host, timeout=args.timeout)
			if '230' in ftp.login():
				#check for bots, if so download the bot
				bot_check(ftp, host)
				ftp.quit()
		except ftplib.all_errors:
			pass


# Init Argument parser
argparser = ArgumentParser(description="Scans targets for anonymous ftp servers - looking for known botnet files.")
argparser.add_argument('targets',
	nargs='*')
argparser.add_argument('-t', '--threads',
	action='store',
	default=10,
	type=int,
	dest='maxThreads',
	help='Number of threads to use, default is 10')
argparser.add_argument('-w', '--wait',
	action='store',
	default=2,
	type=int,
	dest='timeout',
	help='Seconds to wait before timeout, default is 2')
argparser.add_argument('-s', '--shuffle',
	action='store_true',
	default=False,
	dest='shuffle',
	help='Shuffle the target list')
args = argparser.parse_args()

# Check if we are running in a pipe and read from STDIN
if not sys.stdin.isatty():
	args.targets = sys.stdin.readlines()

# Add target IPs/Networks to a netaddr-IPSet
targetSet = IPSet()
for t in args.targets:
	targetSet.add(t)

#output dir
check_output()

# Render IPSets to a list
targetlist = list()
for ip in targetSet:
	targetlist.append(str(ip))

# Check for shuffle argument
if args.shuffle:
	shuffle(targetlist)

# Split list into [maxThreads] smaller batches
targetlist = split_list(targetlist, args.maxThreads)

# Launch threads
for batch in targetlist:
	threading.Thread(target=try_ftp_login, args=(batch,)).start()
