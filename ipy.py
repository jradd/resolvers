import json
from os import path
import sys
from simple_http import http_get
from public.gif3 import handler
import re


   
#URL = 'https://download.dnscrypt.info/dnscrypt-resolvers/json/public-resolvers.json'
#with open('public-resolvers.json', 'w') as f:

#    for line in http_get(URL):
#        f.write(line)

#    data = json.loads(f.read())


ooh = handler('public-resolvers.json3', 'public-resolvers3-copy.json')

#with open('public-resolvers.json', 'r') as f:
#    d = f.read()
#    data = json.loads(d)

with open('public-resolvers.json3', 'rb+') as f:
    d = f.read()
    data = json.loads(d)



newList = [list(tuple((x['country'], x['stamp'], x['proto'], x['addrs'])))
           for x in data
           if x['dnssec'] and x['nofilter'] and x['nolog'] is True]

filterTrue = [list(tuple((x['country'], x['stamp'], x['proto'], x['addrs'])))
           for x in data
           if x['dnssec'] and x['nolog'] is True]


iplist=list()
pattern = r'(?P<ipv4>\d{1,3}\.\d{1,3}\d{1,3}\d{1,3})'
s = ""
for j in range(len(newList)):
    if 'DNSCrypt' in newList[j][2]:
        if isinstance(newList[j][-1], str):
            iplist.append(newList[j][-1])
        else:
            for ip in newList[j][3]:
                if isinstance(ip, str):
                    s+=f' {newList[j][0]}: {ip}\r\n'
                    iplist.insert(j, (newList[j][0], newList[j][-1]))

#m = re.search(pattern, ss)
#print('valid\r\n', m.group(0))
ipv4list=list()
#entries = re.split('\n+', s)
#ipv4=[re.split('?\w+\: ', entry, 2) for entry in entries if re.compile(pattern)]
for item in iplist:
    for p in item[1]:
        if isinstance(p, str):
            match = re.search(pattern, p)
            if match:
                ipv4list.append((item[0], p))
        else:
            print(p)
print(sorted(ipv4list))
print('--------- ipv4 addrs ------------ ')
print(f'{len(ipv4list)} servers with ipv4 addrs.')
idx = 0
stamps, server_list = [], []

for x in filterTrue:
#    if 'DoH' in x[2]:
#        if 'China' in x[0]:
#            print('cool')
#        stamps.append('[static.\'{}-{}\'],stamp = {}'.format(
#          x[0], idx, repr(x[1]), end=' '))
#        server_list.append(('{}-{}'.format(x[0], idx)))
#        idx = idx + 1
#
    if 'DNSCrypt' in x[2]:
            idx=0
            stamps.append('[static.\'{}-{}\'],stamp = {}'.format(
              x[0], idx, repr(x[1]), end=' '))
            server_list.append(('{}-{}'.format(x[0], idx)))
#            idx = idx + 1
#

slist_str = repr([format(x) for x in server_list[:]][:])
s = repr(stamps)



I=set()
rstring = 'servers-{}.txt'
for i in range(100):
    I.add(i)
    if path.exists(rstring.format(i)):
        I.remove(i)
        print('file exists: {}'.format(repr(rstring.format(i))))
t = I.pop()
newfile = rstring.format(t)

with open(newfile, 'w') as f:
    for line in slist_str:
        f.write(line)
    for line in s:
        f.write(line)
