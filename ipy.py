import json
from os import path
import sys
import simple_http

URL = 'https://download.dnscrypt.info/dnscrypt-resolvers/json/public-resolvers.json'
if sys.argv[1] == 'get':
    simple_http.http_get(URL)


with open('public-resolvers.json') as f:
    d = f.read()
    data = json.loads(d)

newList = [list(tuple((x['country'], x['stamp'], x['proto'])))
           for x in data
           if x['dnssec'] and x['nofilter'] and x['nolog'] is True]

idx = 0
stamps, server_list = [], []
for x in newList:
    if 'DNSCrypt' in x[2]:
        stamps.append('[static.\'{}-{}\'],stamp = {}'.format(
          x[0], idx, repr(x[1]), end=' '))
        server_list.append(('{}-{}'.format(x[0], idx)))
#        idx = idx + 1
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
